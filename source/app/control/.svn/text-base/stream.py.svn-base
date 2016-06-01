#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: stream.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-16 15:32:19
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



class streamBase:
    def checkPrivileg(self, streamName="", streamType="", operator="", role="developer"):
        if len(streamName) == 0 or len(streamType) == 0 or len(operator) == 0:
            return (False, "bad argument")

        SQL = """
        SELECT `%s`
        FROM   `tbl_stream_info`
        WHERE  `stream_name`='%s' AND `stream_type`='%s' LIMIT 1""" % (role, streamName, streamType)
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "stream not exist")

        roleList = msg[0].split(',')
        if operator not in roleList: return (False, "permission denied")

        return (True, None)



class add:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                creator     = None,
                stream_name = None,
                stream_type = None,
                desc        = None,
                config      = None,
                crontab     = None)

        try:
            creator     = input.creator
            stream_name = input.stream_name
            stream_type = input.stream_type
            desc        = input.desc
            config      = input.config
            crontab     = input.crontab
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == creator:     return sendResponse('fail', 'missing creator')
        if None == stream_name: return sendResponse('fail', 'missing stream name')
        if None == stream_type: return sendResponse('fail', 'missing stream type')
        if None == desc:        return sendResponse('fail', 'missing description')
        if None == config:      return sendResponse('fail', 'missing config')

        (ret, msg) = UdMySQL(conf.db).insert("tbl_stream_info", {
            "stream_name" : stream_name,
            "stream_type" : stream_type,
            "desc"        : desc,
            "config"      : config,
            "manager"     : creator,
            "developer"   : creator,
            "observer"    : "",
            "crontab"     : crontab or "",
            "status"      : "develop",
            "creator"     : creator,
            "modifier"    : creator,
            "ctime"       : now(),
            "mtime"       : now()})
        if ret == False:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success')



class modify:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                operator    = None,
                stream_name = None,
                stream_type = None,
                desc        = None,
                config      = None,
                crontab     = None,
                manager     = None,
                developer   = None,
                observer    = None,
                status      = None)

        try:
            operator    = input.operator
            stream_name = input.stream_name
            stream_type = input.stream_type
            desc        = input.desc
            config      = input.config
            crontab     = input.crontab
            manager     = input.manager
            developer   = input.developer
            observer    = input.observer
            status      = input.status
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator:    return sendResponse('fail', 'missing operator')
        if None == stream_name: return sendResponse('fail', 'missing stream name')
        if None == stream_type: return sendResponse('fail', 'missing stream type')

        (ret, msg) = streamBase().checkPrivileg(stream_name, stream_type, operator)
        if False == ret: return sendResponse('fail', msg)

        updateDict = {}
        if desc:      updateDict['desc']      = desc
        if config:    updateDict['config']    = config
        if crontab:   updateDict['crontab']   = crontab
        if manager:   updateDict['manager']   = manager
        if developer: updateDict['developer'] = developer
        if observer:  updateDict['observer']  = observer
        if status:    updateDict['status']    = status.lower()
        if len(updateDict) == 0: return sendResponse('fail', "nothing need to do")

        updateDict['modifier'] = operator
        updateDict['mtime']    = now()
        (ret, msg) = UdMySQL(conf.db).update("tbl_stream_info", updateDict,
                "`stream_name`='%s' AND `stream_type`='%s'" % (stream_name, stream_type))

        if False == ret:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success')
    #end for def POST(self):



class list:
    def GET(self):
        SQL = """
        SELECT `stream_id`, `stream_name`, `stream_type`, `desc`, `config`, `manager`, `developer`,
               `observer`, `crontab`, `status`, `creator`, `ctime`, `modifier`, `mtime`
        FROM   `tbl_stream_info`"""
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL, format="dict")
        if False == ret: return sendResponse('fail', msg)

        for row in msg:
            row["ctime"] = str(row["ctime"])
            row["mtime"] = str(row["mtime"])
        return sendResponse('success', msg)


    def POST(self):
        return web.notfound()



class detail:
    def GET(self):
        input = web.input(
                stream_name = None,
                stream_type = None,
                verbose     = "all")

        try:
            stream_name = input.stream_name
            stream_type = input.stream_type
            verbose     = input.verbose
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == stream_name: return sendResponse('fail', 'missing stream name')
        if None == stream_type: return sendResponse('fail', 'missing stream type')

        # 获取stream信息
        SQL = """
        SELECT `stream_id`, `stream_name`, `stream_type`, `desc`, `config`, `manager`, `developer`,
               `observer`, `crontab`, `status`, `creator`, `ctime`, `modifier`, `mtime`
        FROM   `tbl_stream_info`
        WHERE  `stream_name`='%s' AND `stream_type`='%s'""" % (stream_name, stream_type)
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL, format="dict")
        if False == ret: return sendResponse('fail', msg)
        if None  == msg: return sendResponse('fail', "stream not exist")
        streamInfo = msg
        streamInfo["ctime"] = str(streamInfo["ctime"])
        streamInfo["mtime"] = str(streamInfo["mtime"])

        # 获取task信息
        taskCond = "all" == verbose and "1=1" or "`status`='release'"
        SQL = """
        SELECT t.id as `task_id`, t.stream_id as `stream_id`, t.task_name as `task_name`,
               t.task_version as `task_version`, t.desc as `desc`, t.config as `config`,
               t.tool_name as `tool_name`, t.tool_version as `tool_version`, t.depend_task as `depend_task`,
               t.crontab as `crontab`, t.timeout as `timeout`, t.need_retry as `need_retry`,
               t.retry_maxnum as `retry_maxnum`, t.retry_interval as `retry_interval`,
               t.expect_start as `expect_start`, t.expect_finish as `expect_finish`,
               t.err_mail_list as `err_mail_list`, t.err_phone_list as `err_phone_list`,
               t.not_start_mail_list as `not_start_mail_list`,
               t.not_start_phone_list as `not_start_phone_list`,
               t.not_finish_mail_list as `not_finish_mail_list`,
               t.not_finish_phone_list as `not_finish_phone_list`,
               t.alarm_repeat as `alarm_repeat`, t.alarm_interval as `alarm_interval`,
               t.callback_list as `callback_list`, t.developer as `developer`,
               t.observer as `observer`, t.creator as `creator`, t.ctime as `ctime`,
               t.modifier as `modifier`, t.mtime as `mtime`, t.status as `status`
        FROM   tbl_task_info t
        JOIN   (SELECT `id`, `task_name`, max(`task_version`) as `task_version`
                FROM   `tbl_task_info`
                WHERE  `stream_id`=%s AND %s
                GROUP BY `task_name`) temp
        ON     t.id=temp.id
        ORDER BY t.id""" % (streamInfo["stream_id"], taskCond)
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL, format="dict")
        if False == ret: return sendResponse('fail', msg)
        for row in msg:
            row['ctime'] = str(row['ctime'])
            row['mtime'] = str(row['mtime'])

        # 如果verbose为all，则直接返回
        if "all" == verbose:
            streamInfo["tasks"] = msg
            return sendResponse('success', streamInfo)

        # 剔除没有依赖的任务
        for row in msg:
            task_id     = row["task_id"]
            task_name   = row["task_name"]
            depend_task = row["depend_task"]
            (ret, depend_task_id_list) = self._getDependIdList(msg, depend_task)

            #依赖不满足，删除此任务
            if False == ret:
                msg.remove(row)

            #依赖任务的ID比任务自身的ID大，删除此任务，依赖不合法
            for t in depend_task_id_list:
                if t >= task_id:
                    msg.remove(row)
        #end for row in msg:

        # 再检查一次
        for row in msg:
            task_id     = row["task_id"]
            task_name   = row["task_name"]
            depend_task = row["depend_task"]
            (ret, depend_task_id_list) = self._getDependIdList(msg, depend_task)
            if False == ret: return sendResponse('fail', "bad stream information")
        #end for row in msg:

        streamInfo["tasks"] = msg
        return sendResponse('success', streamInfo)


    def POST(self):
        return web.notfound()


    def _getDependIdList(self, rows, depend_task):
        # 检查依赖的任务是否存在，并返回其ID列表
        # 如果无依赖，返回True, []
        # 如果有依赖，并且依赖的任务全都存在，返回True, [id_list]
        # 如果有依赖，并且其依赖的任务中有不存在的，返回False, []
        if len(rows)==0 or len(depend_task)==0:
            return (True, [])

        depend_task_id_list = []
        depend_task_list = depend_task.split(",")
        for row in rows:
            task_id   = row["task_id"]
            task_name = row["task_name"]
            if task_name in depend_task_list:
                depend_task_id_list.append(task_id)
        #end for row in rows:
        if len(depend_task_list) == len(depend_task_id_list):
            return (True, depend_task_id_list)
        else:
            return (False, [])
