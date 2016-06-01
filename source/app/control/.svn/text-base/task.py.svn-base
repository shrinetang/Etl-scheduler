#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: task.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-16 19:14:28
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



class taskBase:
    def checkPrivileg(self, taskName="", taskVersion="", operator="", role="developer"):
        if len(taskName) == 0 or len(taskVersion) == 0 or len(operator) == 0:
            return (False, "bad argument")

        SQL = """
        SELECT   `%s`
        FROM     `tbl_task_info`
        WHERE    `task_name`='%s' AND `task_version`=%s
        LIMIT 1""" % (role, taskName, taskVersion)
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "task or version not exist")

        roleList = msg[0].split(',')
        if operator not in roleList: return (False, "permission denied")

        return (True, None)


    def checkStream(self, streamId = ""):
        if len(streamId) == 0:
            return (False, "bad stream id")

        SQL = "SELECT `stream_id` FROM `tbl_stream_info` WHERE `stream_id`=%s LIMIT 1""" % streamId
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "stream not exist")

        return (True, None)


    def checkTool(self, toolName = "", toolVersion = ""):
        if len(toolName) == 0 or len(toolVersion) == 0:
            return (False, "bad tool information")

        SQL = """
        SELECT `status`
        FROM   `tbl_tool_info`
        WHERE  `tool_name`='%s' AND `tool_version`=%s LIMIT 1""" % (toolName, toolVersion)
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "tool or version not exist")

        if "release" != msg[0]:
            return (False, "tool or version not a release version")
        else:
            return (True, None)


    def checkDepend(self, streamId = "", taskName = "", taskDepend = ""):
        if len(streamId) == 0 or len(taskName) == 0 or len(taskDepend) == 0:
            return (False, "bad depend information")

        taskId = None
        SQL = """
        SELECT `id`
        FROM   `tbl_task_info`
        WHERE  `stream_id`=%s AND `task_name`='%s' LIMIT 1""" % (streamId, taskName)
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return (False, msg)
        if None  != msg: taskId = msg[0]

        dependList = taskDepend.split(",")
        for dependEntry in dependList:
            SQL = """
            SELECT `id`
            FROM   `tbl_task_info`
            WHERE  `stream_id`=%s AND `task_name`='%s' LIMIT 1""" % (streamId, dependEntry)
            (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
            if False == ret: return (False, msg)
            if None  == msg: return (False, "%s not exist" % dependEntry)

            if taskId != None and msg[0] >= taskId:
                return (False, "%s ge %s" % (dependEntry, taskName))

        return (True, None)


    def checkRelease(self, taskName=""):
        if len(taskName) == 0:
            return (False, "bad argument")

        SQL = "SELECT `status` FROM `tbl_task_info` WHERE `task_name`='%s'" % taskName
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "task not exist")

        for (status,) in msg:
            if status == 'release':
                return (False, "release version is exist")

        return (True, None)



class add:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                creator               = None,
                stream_id             = None,
                task_name             = None,
                desc                  = None,
                config                = None,
                tool_name             = None,
                tool_version          = None,
                depend_task           = None,
                expect_start          = None,
                expect_finish         = None,
                crontab               = None,
                timeout               = None,
                need_retry            = None,
                retry_maxnum          = None,
                retry_interval        = None,
                err_mail_list         = None,
                err_phone_list        = None,
                not_start_mail_list   = None,
                not_start_phone_list  = None,
                not_finish_mail_list  = None,
                not_finish_phone_list = None,
                alarm_repeat          = None,
                alarm_interval        = None,
                callback_list         = None)

        try:
            creator               = input.creator
            stream_id             = input.stream_id
            task_name             = input.task_name
            desc                  = input.desc
            config                = input.config
            tool_name             = input.tool_name
            tool_version          = input.tool_version
            depend_task           = input.depend_task
            expect_start          = input.expect_start
            expect_finish         = input.expect_finish
            crontab               = input.crontab
            timeout               = input.timeout
            need_retry            = input.need_retry
            retry_maxnum          = input.retry_maxnum
            retry_interval        = input.retry_interval
            err_mail_list         = input.err_mail_list
            err_phone_list        = input.err_phone_list
            not_start_mail_list   = input.not_start_mail_list
            not_start_phone_list  = input.not_start_phone_list
            not_finish_mail_list  = input.not_finish_mail_list
            not_finish_phone_list = input.not_finish_phone_list
            alarm_repeat          = input.alarm_repeat
            alarm_interval        = input.alarm_interval
            callback_list         = input.callback_list
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == creator       : return sendResponse('fail', 'missing creator')
        if None == stream_id     : return sendResponse('fail', 'missing stream id')
        if None == task_name     : return sendResponse('fail', 'missing task name')
        if None == desc          : return sendResponse('fail', 'missing description')
        if None == config        : return sendResponse('fail', 'missing config')
        if None == tool_name     : return sendResponse('fail', 'missing tool name')
        if None == tool_version  : return sendResponse('fail', 'missing tool version')
        if None == expect_start  : return sendResponse('fail', 'missing expect start time')
        if None == expect_finish : return sendResponse('fail', 'missing expect finish time')

        (ret, msg) = taskBase().checkStream(stream_id)
        if False == ret: return sendResponse('fail', msg)

        (ret, msg) = taskBase().checkTool(tool_name, tool_version)
        if False == ret: return sendResponse('fail', msg)

        if None != depend_task and len(depend_task) > 0:
            (ret, msg) = taskBase().checkDepend(stream_id, task_name, depend_task)
            if False == ret: return sendResponse('fail', msg)

        (ret, msg) = UdMySQL(conf.db).insert("tbl_task_info", {
            "stream_id"             : stream_id,
            "task_name"             : task_name,
            "task_version"          : "1",
            "desc"                  : desc,
            "config"                : config,
            "tool_name"             : tool_name,
            "tool_version"          : tool_version,
            "expect_start"          : expect_start,
            "expect_finish"         : expect_finish,
            "depend_task"           : depend_task           or "",
            "crontab"               : crontab               or "",
            "timeout"               : timeout               or "24",
            "need_retry"            : need_retry            or "0",
            "retry_maxnum"          : retry_maxnum          or "3",
            "retry_interval"        : retry_interval        or "30",
            "err_mail_list"         : err_mail_list         or "",
            "err_phone_list"        : err_phone_list        or "",
            "not_start_mail_list"   : not_start_mail_list   or "",
            "not_start_phone_list"  : not_start_phone_list  or "",
            "not_finish_mail_list"  : not_finish_mail_list  or "",
            "not_finish_phone_list" : not_finish_phone_list or "",
            "alarm_repeat"          : alarm_repeat          or "0",
            "alarm_interval"        : alarm_interval        or "30",
            "callback_list"         : callback_list         or "",
            "developer"             : creator,
            "observer"              : "",
            "creator"               : creator,
            "ctime"                 : now(),
            "modifier"              : creator,
            "mtime"                 : now(),
            "status"                : "develop"})
        if ret == False:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success')
    # end for def POST(self):



class modify:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                operator              = None,
                stream_id             = None,
                task_name             = None,
                task_version          = None,
                desc                  = None,
                config                = None,
                tool_name             = None,
                tool_version          = None,
                depend_task           = None,
                expect_start          = None,
                expect_finish         = None,
                crontab               = None,
                timeout               = None,
                need_retry            = None,
                retry_maxnum          = None,
                retry_interval        = None,
                err_mail_list         = None,
                err_phone_list        = None,
                not_start_mail_list   = None,
                not_start_phone_list  = None,
                not_finish_mail_list  = None,
                not_finish_phone_list = None,
                alarm_repeat          = None,
                alarm_interval        = None,
                callback_list         = None,
                developer             = None,
                observer              = None,
                status                = None)

        try:
            operator              = input.operator
            stream_id             = input.stream_id
            task_name             = input.task_name
            task_version          = input.task_version
            desc                  = input.desc
            config                = input.config
            tool_name             = input.tool_name
            tool_version          = input.tool_version
            depend_task           = input.depend_task
            expect_start          = input.expect_start
            expect_finish         = input.expect_finish
            crontab               = input.crontab
            timeout               = input.timeout
            need_retry            = input.need_retry
            retry_maxnum          = input.retry_maxnum
            retry_interval        = input.retry_interval
            err_mail_list         = input.err_mail_list
            err_phone_list        = input.err_phone_list
            not_start_mail_list   = input.not_start_mail_list
            not_start_phone_list  = input.not_start_phone_list
            not_finish_mail_list  = input.not_finish_mail_list
            not_finish_phone_list = input.not_finish_phone_list
            alarm_repeat          = input.alarm_repeat
            alarm_interval        = input.alarm_interval
            callback_list         = input.callback_list
            developer             = input.developer
            observer              = input.observer
            status                = input.status
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator:     return sendResponse('fail', 'missing operator')
        if None == stream_id:    return sendResponse('fail', 'missing stream id')
        if None == task_name:    return sendResponse('fail', 'missing task name')
        if None == task_version: return sendResponse('fail', 'missing task version')

        (ret, msg) = taskBase().checkPrivileg(task_name, task_version, operator)
        if False == ret: return sendResponse('fail', msg)

        if None != tool_name and None != tool_version:
            (ret, msg) = taskBase().checkTool(tool_name, tool_version)
            if False == ret: return sendResponse('fail', msg)

        if None != depend_task and len(depend_task) > 0:
            (ret, msg) = taskBase().checkDepend(stream_id, task_name, depend_task)
            if False == ret: return sendResponse('fail', msg)

        if None != status:
            status = status.lower()
            if "release" == status:
                (ret, msg) = taskBase().checkRelease(task_name)
                if False == ret: return sendResponse('fail', msg)

        updateDict = {}
        if desc                  : updateDict['desc']                  = desc
        if config                : updateDict['config']                = config
        if tool_name             : updateDict['tool_name']             = tool_name
        if tool_version          : updateDict['tool_version']          = tool_version
        if depend_task           : updateDict['depend_task']           = depend_task
        if expect_start          : updateDict['expect_start']          = expect_start
        if expect_finish         : updateDict['expect_finish']         = expect_finish
        if crontab               : updateDict['crontab']               = crontab
        if timeout               : updateDict['timeout']               = timeout
        if need_retry            : updateDict['need_retry']            = need_retry
        if retry_maxnum          : updateDict['retry_maxnum']          = retry_maxnum
        if retry_interval        : updateDict['retry_interval']        = retry_interval
        if err_mail_list         : updateDict['err_mail_list']         = err_mail_list
        if err_phone_list        : updateDict['err_phone_list']        = err_phone_list
        if not_start_mail_list   : updateDict['not_start_mail_list']   = not_start_mail_list
        if not_start_phone_list  : updateDict['not_start_phone_list']  = not_start_phone_list
        if not_finish_mail_list  : updateDict['not_finish_mail_list']  = not_finish_mail_list
        if not_finish_phone_list : updateDict['not_finish_phone_list'] = not_finish_phone_list
        if alarm_repeat          : updateDict['alarm_repeat']          = alarm_repeat
        if alarm_interval        : updateDict['alarm_interval']        = alarm_interval
        if callback_list         : updateDict['callback_list']         = callback_list
        if developer             : updateDict['developer']             = developer
        if observer              : updateDict['observer']              = observer
        if status                : updateDict['status']                = status
        if len(updateDict) == 0: return sendResponse('fail', "nothing need to do")

        updateDict['modifier'] = operator
        updateDict['mtime']    = now()
        (ret, msg) = UdMySQL(conf.db).update("tbl_task_info", updateDict,
                "`stream_id`=%s AND `task_name`='%s' AND `task_version`=%s" % (stream_id, task_name, task_version))

        if False == ret:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success')
    #end for def POST(self):



class upgrade:
    def GET(self):
        return web.notfound()


    def POST(self):
        input = web.input(
                operator     = None,
                task_name    = None)

        try:
            operator      = input.operator
            task_name     = input.task_name
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator:  return sendResponse('fail', 'missing operator')
        if None == task_name: return sendResponse('fail', 'missing task name')

        SQL = "SELECT max(`task_version`) FROM tbl_task_info WHERE task_name='%s'" % task_name
        (ret, msg) = UdMySQL(conf.db).queryRow(SQL)
        if False == ret: return sendResponse('fail', msg)
        if None  == msg: return sendResponse('fail', 'task not exist')

        cur_task_version = msg[0]
        (ret, msg) = taskBase().checkPrivileg(task_name, str(cur_task_version), operator)
        if False == ret: return sendResponse('fail', msg)

        SQL = """
        INSERT INTO `tbl_task_info` (
               `stream_id`, `task_name`, `task_version`, `desc`, `config`,
               `tool_name`, `tool_version`, `depend_task`, `crontab`, `timeout`, `need_retry`,
               `retry_maxnum`, `retry_interval`, `expect_start`, `expect_finish`, `err_mail_list`,
               `err_phone_list`, `not_start_mail_list`, `not_start_phone_list`,
               `not_finish_mail_list`, `not_finish_phone_list`, `alarm_repeat`,
               `alarm_interval`, `callback_list`, `developer`, `observer`, `creator`, `ctime`,
               `modifier`, `mtime`, `status` )
        SELECT `stream_id`, `task_name`, `task_version`+1 as `task_version`, `desc`, `config`,
               `tool_name`, `tool_version`, `depend_task`, `crontab`, `timeout`, `need_retry`,
               `retry_maxnum`, `retry_interval`, `expect_start`, `expect_finish`, `err_mail_list`,
               `err_phone_list`, `not_start_mail_list`, `not_start_phone_list`,
               `not_finish_mail_list`, `not_finish_phone_list`, `alarm_repeat`,
               `alarm_interval`, `callback_list`, `developer`, `observer`, `creator`, `ctime`,
               '%s' as `modifier`, '%s' as `mtime`, 'develop' as `status`
        FROM   `tbl_task_info`
        WHERE  `task_name`='%s' AND `task_version`=%s""" % (operator, now(), task_name, cur_task_version)
        (ret, msg) = UdMySQL(conf.db).execute(SQL)
        if False == ret:
            return sendResponse('fail', msg)
        else:
            return sendResponse('success', cur_task_version+1)
    #end for def POST(self):



class list:
    def GET(self):
        input = web.input(stream_id = None)

        try:
            stream_id = input.stream_id
        except Exception as e:
            return sendResponse('fail', str(e))

        streamCond = "1=1"
        if None != stream_id and len(stream_id) > 0:
            streamCond = "stream_id=%s" % stream_id

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
                WHERE  %s
                GROUP BY `task_name`) temp
        ON     t.id=temp.id""" % streamCond
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
        input = web.input(task_name = None)

        try:
            task_name = input.task_name
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == task_name: return sendResponse('fail', 'missing task name')

        SQL = """
        SELECT `id`, `stream_id`, `task_name`, `task_version`, `desc`, `config`, `tool_name`, `tool_version`,
               `depend_task`, `crontab`, `timeout`, `need_retry`, `retry_maxnum`, `retry_interval`, `expect_start`,
               `expect_finish`, `err_mail_list`, `err_phone_list`, `not_start_mail_list`, `not_start_phone_list`,
               `not_finish_mail_list`, `not_finish_phone_list`, `alarm_repeat`, `alarm_interval`, `callback_list`,
               `developer`, `observer`, `creator`, `ctime`, `modifier`, `mtime`, `status`
        FROM   tbl_task_info
        WHERE  task_name='%s'""" % task_name
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL, format="dict")
        if False == ret:      return sendResponse('fail', msg)
        if 0     == len(msg): return sendResponse('fail', 'task not exist')

        for row in msg:
            row["ctime"] = str(row["ctime"])
            row["mtime"] = str(row["mtime"])
        return sendResponse('success', msg)


    def POST(self):
        return web.notfound()
