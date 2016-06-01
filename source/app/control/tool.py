#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: tool.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-10 18:18:02
#  Author: huabo (daijun), caodaijun@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2013 ---
#                              All Rights Reserved.
# ============================================================================
import web
from utils.ud_base   import sendResponse, now
from utils.ud_mysql  import UdMySQL
from utils.ud_config import conf



class toolBase:
    def checkPrivileg(self, toolName="", toolVersion="", operator="", role="developer"):
        if len(toolName) == 0 or len(toolVersion) == 0 or len(operator) == 0:
            return (False, "bad argument")

        SQL = """
        SELECT `%s`
        FROM   `tbl_tool_info`
        WHERE  `tool_name`='%s' AND `tool_version`=%s LIMIT 1""" % (role, toolName, toolVersion)
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "tool or version not exist")

        roleList = msg[0].split(',')
        if operator not in roleList: return (False, "permission denied")

        return (True, None)



class add:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                creator   = None,
                tool_name = None,
                desc      = None,
                config    = None)

        try:
            creator   = input.creator
            tool_name = input.tool_name
            desc      = input.desc
            config    = input.config
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == creator:   return sendResponse('fail', 'missing creator')
        if None == tool_name: return sendResponse('fail', 'missing tool name')
        if None == desc:      return sendResponse('fail', 'missing description')
        if None == config:    return sendResponse('fail', 'missing config')

        (ret, msg) = UdMySQL(conf.db).insert("tbl_tool_info", {
            "tool_name"    : tool_name,
            "tool_version" : "1",
            "desc"         : desc,
            "config"       : config,
            "status"       : "develop",
            "creator"      : creator,
            "developer"    : creator,
            "modifier"     : creator,
            "ctime"        : now(),
            "mtime"        : now()})
        if False == ret:
             return sendResponse('fail', msg)
        else:
            return sendResponse('success')



class modify:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                operator     = None,
                tool_name    = None,
                tool_version = None,
                desc         = None,
                config       = None,
                developer    = None,
                status       = None)

        try:
            operator     = input.operator
            tool_name    = input.tool_name
            tool_version = input.tool_version
            desc         = input.desc
            config       = input.config
            developer    = input.developer
            status       = input.status
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator:     return sendResponse('fail', 'missing operator')
        if None == tool_name:    return sendResponse('fail', 'missing tool name')
        if None == tool_version: return sendResponse('fail', 'missing tool version')

        (ret, msg) = toolBase().checkPrivileg(tool_name, tool_version, operator)
        if False == ret: return sendResponse('fail', msg)

        updateDict = {}
        if desc:      updateDict['desc']      = desc
        if config:    updateDict['config']    = config
        if developer: updateDict['developer'] = developer
        if status:    updateDict['status']    = status.lower()
        if len(updateDict) == 0: return sendResponse('fail', "nothing need to do")

        updateDict['modifier'] = operator
        updateDict['mtime']    = now()
        (ret, msg) = UdMySQL(conf.db).update("tbl_tool_info", updateDict,
                "`tool_name`='%s' AND `tool_version`=%s" % (tool_name, tool_version))
        if False == ret:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success')



class upgrade:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                operator  = None,
                tool_name = None)

        try:
            operator  = input.operator
            tool_name = input.tool_name
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator:  return sendResponse('fail', 'missing operator')
        if None == tool_name: return sendResponse('fail', 'missing tool name')

        #获取当前工具最大版本对应的信息
        SQL = """
        SELECT `tool_name`, `tool_version`, `desc`, `config`, `developer`, `creator`, `ctime`
        FROM   `tbl_tool_info`
        WHERE  `tool_name`='%s' ORDER BY `tool_version` DESC LIMIT 1""" % tool_name
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return sendResponse('fail', msg)
        if None  == msg: return sendResponse('fail', "tool not exist")
        (tool_name, tool_version, desc, config, developer, creator, ctime) = msg

        #判断最新版本的权限
        (ret, msg) = toolBase().checkPrivileg(tool_name, str(tool_version), operator)
        if False == ret: return sendResponse('fail', msg)

        new_tool_version = tool_version + 1
        (ret, msg) = UdMySQL(conf.db).insert("tbl_tool_info", {
            "tool_name"    : tool_name,
            "tool_version" : new_tool_version,
            "desc"         : desc,
            "config"       : config,
            "status"       : "develop",
            "creator"      : creator,
            "developer"    : developer,
            "modifier"     : operator,
            "ctime"        : str(ctime),
            "mtime"        : now()})
        if False == ret:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success', new_tool_version)



class delete:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                operator  = None,
                tool_name = None)

        try:
            operator  = input.operator
            tool_name = input.tool_name
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator  : return sendResponse('fail', 'missing operator')
        if None == tool_name : return sendResponse('fail', 'missing tool name')

        # 获取当前工具的版本列表
        SQL = "SELECT `tool_version` FROM `tbl_tool_info` WHERE `tool_name`='%s'" % tool_name
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL)
        if False == ret:      return sendResponse('fail', msg)
        if 0     == len(msg): return sendResponse('fail', "tool not exist")

        failVersionList = []
        for (tool_version,) in msg:
            (ret, msg) = toolBase().checkPrivileg(tool_name, str(tool_version), operator)
            if False == ret:
                failVersionList.append((tool_version, msg))
                continue

            (ret, msg) = UdMySQL(conf.db).delete("tbl_tool_info",
                    "`tool_name`='%s' AND `tool_version`=%s" % (tool_name, tool_version))
            if False == ret:
                failVersionList.append((tool_version, msg))

        if len(failVersionList) != 0:
            return sendResponse('fail', failVersionList)
        else:
            return sendResponse('success')



class list:
    def GET(self):
        SQL = """
        SELECT t.tool_name as `tool_name`, t.tool_version as `tool_version`, t.desc as `desc`,
               t.config as `config`, t.developer as `developer`, t.creator as `creator`,
               t.ctime as `ctime`, t.modifier as `modifier`, t.mtime as `mtime`
        FROM   `tbl_tool_info` t
        JOIN   (SELECT `tool_name`, max(`tool_version`) as `tool_version`
                FROM   `tbl_tool_info`
                GROUP BY `tool_name`) temp
        ON     t.tool_name=temp.tool_name and t.tool_version=temp.tool_version"""
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL, format="dict")
        if False == ret: return sendResponse('fail', msg)

        for row in msg:
            row['ctime'] = str(row['ctime'])
            row['mtime'] = str(row['mtime'])
        return sendResponse('success', msg)


    def POST(self):
        return web.notfound()



class detail:
    def GET(self):
        input = web.input(tool_name = None)

        try:
            tool_name = input.tool_name
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == tool_name: return sendResponse('fail', 'missing tool name')

        SQL = """
        SELECT `tool_name`, `tool_version`, `desc`, `config`, `developer`,
               `status`, `creator`, `ctime`, `modifier`, `mtime`
        FROM   `tbl_tool_info`
        WHERE  `tool_name`='%s'""" % tool_name
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL, format="dict")
        if False == ret:      return sendResponse('fail', msg)
        if 0     == len(msg): return sendResponse('fail', 'tool not exist')

        for row in msg:
            row['ctime'] = str(row['ctime'])
            row['mtime'] = str(row['mtime'])
        return sendResponse('success', msg)


    def POST(self):
        return web.notfound()
