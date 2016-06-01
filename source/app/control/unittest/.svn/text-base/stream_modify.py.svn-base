#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: stream_modify.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-15 15:06:46
#  Author: huabo (daijun), caodaijun@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2013 ---
#                              All Rights Reserved.
# ============================================================================


import json
import urllib
import httplib


def main():
    host = 'cq01-test-nlp1.cq01.baidu.com:8962'

    httpParams = urllib.urlencode({
         "operator"    : "caodaijun",
         "stream_name" : "ps",
         "stream_type" : "day",
         "developer"   : "caodaijun,zuojingchao"
    })
    httpHeaders = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/plain"}
    conn = httplib.HTTPConnection(host)
    conn.request("POST", "/stream/modify", httpParams, httpHeaders)
    response = conn.getresponse()
    print response.read()


if __name__ == "__main__":
    main()
