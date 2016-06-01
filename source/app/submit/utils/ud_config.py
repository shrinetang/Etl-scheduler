#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: ud_config.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-04-15 15:35:03
#  Author: huabo (daijun), caodaijun@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2013 ---
#                              All Rights Reserved.
# ============================================================================


class Config(object):
    def __init__(self):
        self.db = {
            'user'     : 'root',
            'password' : 'safe',
            'host'     : '127.0.0.1',
            'port'     : '3306',
            'database' : 'rp_ud_etl',
            'raise_on_warnings' : True,
        }


conf = Config()


if __name__ == "__main__":
    pass
