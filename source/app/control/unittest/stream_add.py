#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: stream_add.py
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
         "creator"     : "caodaijun",
         "stream_name" : "ps",
         "stream_type" : "day",
         "desc"        : "fuck the stream",
         "config"      : "ewoJInBhcnRpdGlvbiI6ICJwYXJ0aXRpb25fc3RhdF9kYXRlPSckKGRhdGUgZm9ybWF0PSJZbWQi\nIG9mZnNldD0iLTEiKSciLAp9\n",
    })
    httpHeaders = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/plain"}
    conn = httplib.HTTPConnection(host)
    conn.request("POST", "/stream/add", httpParams, httpHeaders)
    response = conn.getresponse()
    print response.read()


if __name__ == "__main__":
    main()
