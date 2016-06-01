#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: control.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-10 16:19:13
#  Author: huabo (daijun), caodaijun@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2013 ---
#                              All Rights Reserved.
# ============================================================================
import os
import sys
import web
sys.path.append(os.path.dirname(__file__))


class version:
    def GET(self):
        return "etl control server, version 1.0"


urls = (
    "/tool/add",      "tool.add",
    "/tool/modify",   "tool.modify",
    "/tool/upgrade",  "tool.upgrade",
    "/tool/delete",   "tool.delete",
    "/tool/list",     "tool.list",
    "/tool/detail",   "tool.detail",

    "/stream/add",    "stream.add",
    "/stream/modify", "stream.modify",
    "/stream/list",   "stream.list",
    "/stream/detail", "stream.detail",

    "/stream/instance/list",   "instance.list",
    "/stream/instance/detail", "instance.detail",

    "/task/add",      "task.add",
    "/task/modify",   "task.modify",
    "/task/upgrade",  "task.upgrade",
    "/task/list",     "task.list",
    "/task/detail",   "task.detail",

    "/.*", "version")
application = web.application(urls, globals()).wsgifunc()
