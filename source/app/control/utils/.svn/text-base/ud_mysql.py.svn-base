#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: ud_mysql.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2013-10-18 10:33:17
#  Author: huabo (daijun), caodaijun@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2013 ---
#                              All Rights Reserved.
# ============================================================================


import mysql.connector
from mysql.connector import errorcode



class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None



class UdMySQL(object):
    def __init__(self, dbInfo):
        self._dbInfo = dbInfo
        self._errMsg = None


    def _getDBConn(self):
        try:
            return mysql.connector.connect(**self._dbInfo)
        except mysql.connector.Error as e:
            log.err("connect mysql error, err: %s, mysqlinfo: %s" % (str(e), str(self._dbInfo)))
            self._errMsg = str(e)
            return None


    def insert(self, tableName, columns):
        if len(tableName) == 0 or len(columns) == 0:
            return (False, "bad argument")

        fields = ""
        values = ""
        for field in columns:
            fields = fields + "`"  + field + "`, "
            values = values + "%(" + field + ")s, "
        fields = fields[0:-2]
        values = values[0:-2]

        SQL = "INSERT INTO " + tableName + " (" + fields + ") VALUES (" + values + ")"

        cnx = self._getDBConn()
        if None == cnx:
            return(False, self._errMsg)

        try:
            cursor = cnx.cursor()
            cursor.execute(SQL, columns)
            cursor.close()
            cnx.commit()
            cnx.close()
        except mysql.connector.Error as e:
            return (False, str(e))

        return (True, None)


    def update(self, tableName, columns, condition):
        #为了安全性，condition参数是必须的，如果一定要全表更新，可以将condition设置为1=1
        if len(tableName) == 0 or len(columns) == 0 or len(condition) == 0:
            return (False, "bad argument")

        updateDesc = ''
        for field in columns:
            updateDesc = updateDesc + "`"  + field + "`=%(" + field + ")s, "
        updateDesc = updateDesc[0:-2]

        SQL = "UPDATE " + tableName + " SET " + updateDesc + " WHERE " + condition

        cnx = self._getDBConn()
        if None == cnx:
            return(False, self._errMsg)

        try:
            cursor = cnx.cursor()
            cursor.execute(SQL, columns)
            cursor.close()
            cnx.commit()
            cnx.close()
        except mysql.connector.Error as e:
            return (False, str(e))

        return (True, None)


    def delete(self, tableName, condition):
        #为了安全性，condition参数是必须的，如果一定要清空表，可以将condition设置为1=1
        if len(tableName) == 0 or len(condition) == 0:
            return (False, "bad argument")

        SQL = "DELETE FROM " + tableName + " WHERE " + condition

        cnx = self._getDBConn()
        if None == cnx:
            return(False, self._errMsg)

        try:
            cursor = cnx.cursor()
            cursor.execute(SQL)
            cursor.close()
            cnx.commit()
            cnx.close()
        except mysql.connector.Error as e:
            return (False, str(e))

        return (True, None)


    def execute(self, SQL):
        if len(SQL) == 0:
            return (False, "bad argument")

        cnx = self._getDBConn()
        if None == cnx:
            return(False, self._errMsg)

        try:
            cursor = cnx.cursor()
            cursor.execute(SQL)
            cursor.close()
            cnx.commit()
            cnx.close()
        except mysql.connector.Error as e:
            return (False, str(e))

        return (True, None)


    def queryAll(self, SQL, format="tuple"):
        if len(SQL) == 0:
            return (False, "bad argument")

        cnx = self._getDBConn()
        if None == cnx:
            return(False, self._errMsg)

        rows = None
        try:
            cursor = None
            if format == "dict":
                cursor = cnx.cursor(cursor_class=MySQLCursorDict)
            else:
                cursor = cnx.cursor()

            cursor.execute(SQL)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as e:
            return (False, str(e))

        return (True, rows)


    def queryRow(self, SQL, format="tuple"):
        if len(SQL) == 0:
            return (False, "bad argument")

        cnx = self._getDBConn()
        if None == cnx:
            return(False, self._errMsg)

        rows = None
        try:
            cursor = None
            if format == "dict":
                cursor = cnx.cursor(cursor_class=MySQLCursorDict)
            else:
                cursor = cnx.cursor()

            cursor.execute(SQL)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as e:
            return (False, str(e))

        return (True, len(rows)>0 and rows[0] or None)


    #def createIfTableNotExist(self, tableName, createSQL):
    #    if None == tableName or None == createSQL:
    #        return (False, "bad argument")

    #    checkSQL = "show tables like '%s'" % tableName
    #    (ret, msg) = self.queryRow(checkSQL)
    #    if False == ret:
    #        return (ret, msg)
    #    if None != msg:
    #        return (ret, "table exist")

    #    return self.execute(createSQL)


if __name__ == "__main__":
    pass
