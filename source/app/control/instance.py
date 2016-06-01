#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: instance.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-23 18:24:57
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



class list:
    def GET(self):
        input = web.input(stream_id = None)

        try:
            stream_id = input.stream_id
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == stream_id: return sendResponse('fail', 'missing stream id')

        SQL = """
        SELECT DISTINCT `stream_instance_id`
        FROM   `tbl_task_instance_info`
        WHERE  `stream_id`=%s""" % stream_id
        (ret, msg) = UdMySQL(conf.db).queryAll(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "stream instance not exist")

        return sendResponse('success', msg)


    def POST(self):
        return web.notfound()



class detail:
    def GET(self):
        input = web.input(
                operator           = None,
                stream_id          = None,
                stream_instance_id = None)

        try:
            operator           = input.operator
            stream_id          = input.stream_id
            stream_instance_id = input.stream_instance_id
        except Exception as e:
            return sendResponse('fail', str(e))

        if None == operator:           return sendResponse('fail', 'missing operator')
        if None == stream_id:          return sendResponse('fail', 'missing stream id')
        if None == stream_instance_id: return sendResponse('fail', 'missing stream instance id')

        SQL = """
        SELECT `task_name`, `instance_id`, `depend_idlist`, `config`, `crontab`,
               `ctime`, `queue`, `start`, `finish`, `cur_retry`, `cur_alarm_repeat`,
               `datasize`, `dataline`, `version`, `status`, `status_msg`
        FROM   `tbl_task_instance_info`
        WHERE  `stream_id`=%s AND `stream_instance_id`=%s""" % (stream_id, stream_instance_id)

        (ret, msg) = UdMySQL(conf.db).queryAll(SQL)
        if False == ret: return (False, msg)
        if None  == msg: return (False, "stream instance not exist")

        return sendResponse('success', msg)


    def POST(self):
        return web.notfound()
