#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: ud_base.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-15 13:14:00
#  Author: huabo (daijun), caodaijun@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2013 ---
#                              All Rights Reserved.
# ============================================================================
import json
import time
from datetime import datetime


def sendResponse(status='success', message='None'):
    tempDict = {
        'status':  status,
        'message': message
    }
    return json.dumps(tempDict, indent=2)


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    main()
