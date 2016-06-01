#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: ud_submit.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2014-
#  Author: tangxingyu@baidu.com
# Company: baidu.com
#
#                          --- Copyleft (c), 2014 ---
#                              All Rights Reserved.
# ============================================================================

from utils.ud_base   import sendResponse, now
from utils.ud_mysql  import UdMySQL
from utils.ud_config import conf
import uuid
import time
import sys
import json
import urllib
import httplib
#调试信息打印开关
debug = 1

#提交给control模块的json字符串
post_json=''
host = 'cq01-test-nlp1.cq01.baidu.com:8962'
httpHeaders = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/plain"}

class ud_submit(object):
    """get streams info from mysql，then get related tasks and instance，submit to control"""
    def __init__(self):
        self.file_name = ''
        self.record_streams = []


    #该方法实现从数据库中获取数据流并分类存储
    def submit_instance(self,stream_type):
        #connect mysql to get info
        if debug:
            print 'stream_type is %s' %(stream_type)
        SQL="""
        SELECT stream_id,stream_name,stream_type,crontab
        FROM tbl_stream_info 
        WHERE status='develop' and stream_type='%s'""" % (stream_type)
        (ret,stream_rows)=UdMySQL(conf.db).queryAll(SQL)
        if False == ret: return (False,stream_rows)
        if None == stream_rows: return (False,"stream require fail")
        if 1 == debug:
            print 'stream_rows is : %s' %(stream_rows)

        #读取相应的本地记录的提交文件（带日期，小时等，存入到self.record_streams[]）
        if stream_type == 'hour':
            self.file_name = stream_type + '_' +  time.strftime('%Y-%m-%d-%H') + '.json'
        elif stream_type in ['day','week','month']:
            self.file_name = stream_type + '_' + time.strftime('%Y-%m-%d') + '.json'
        else:
            self.file_name = stream_type + '.json'
        fp = open(self.file_name,'a+')
        for lines in fp:
            stream = json.loads(lines)
            self.record_streams.append(stream[0]['stream_id'])
        fp.close()
        if debug == 1:
            print 'file_name : %s' %(self.file_name)
            print 'record_streams : %s' %(str(self.record_streams))

        for (stream_id,stream_name,stream_type,crontab) in stream_rows:
            if stream_id in self.record_streams:
                continue
            else:
                (ret,info) = self.Instance_stream(stream_id)
                if False == ret: return (False,info)

        return (True,"submit stream info OK")
 

    #该类实现对数据流的实例化和封装
    def Instance_stream(self,stream_id):
        if(stream_id == None  or stream_id <= 0):
            return(False)

        SQL="""
        SELECT id,stream_id,task_name,depend_task,status
        FROM tbl_task_info
        WHERE stream_id='%s' and status='release' 
        ORDER BY id
        """ % (stream_id)
        if 1 == debug:
            print stream_id,SQL
        (ret,task_rows)=UdMySQL(conf.db).queryAll(SQL)
        if False == ret: return (False,task_rows)
        if None == task_rows: return (False,"task require fail")
        if 1 == debug:
            print 'stream_id : %s' %(stream_id)
            print 'SQL       : %s' %(SQL)
            print 'task_rows : %s' %(`task_rows`)
        
        stream_instance = []
        #give all task instance id     
        task_instance_uuid = {}
        task_instance_id ={} 
        for (task_id,stream_id,task_name,depend_task,status) in task_rows:
            task_instance_id[task_name] = task_id
            task_instance_uuid[task_name] = str(uuid.uuid1())

        #submit 
        for (task_id,stream_id,task_name,depend_task,status) in task_rows:
            #check each dependtask is instance or not
            task_instance={}
            depend_num = 0
            for eachtask in depend_task:
                if eachtask in task_instance_idlist.keys:
                    if task_instance_id['eachtask'] < task_id:
                        task_instance.setdefault('depend_idlist',[]).append(task_instance_uuid['eachtask'])
                        depend_num += 1
                    else:
                        continue
            if depend_num == len(depend_task):
                #instance this task
                task_instance['id'] = task_id
                task_instance['stream_id'] = stream_id
                task_instance['task_name'] = task_name
                task_instance['status'] = status 
                task_instance['instance_id'] = task_instance_uuid[task_name]
                stream_instance.append(task_instance)
                if debug == 1:
                    print 'task_instance  : %s' %(`task_instance`)
                    print 'stream_instance: %s' %(`stream_instance`) 
            else:
                print '%s : depend_tasks instanceid is not completed' %(task_name)
                continue

        post_json_stream = json.dumps(stream_instance)
        if debug == 1:
            print 'post_json_stream : %s' %(str(post_json_stream))
            
        (ret,info) = self.POST(post_json_stream)
        #post success then write stream_json 
        if True == ret:
            fp = open(self.file_name,'a')
            if self.record_streams:
                fp.write('\n')
            fp.write(post_json_stream)
            fp.close()
        return (True,"instance stream %d OK" %(stream_id))

       
    #该类实现将封装好的数据流实例表发送给control模块
    def POST(self,json_stream):
        print 'post :%s' %(str(json_stream))
        #httpParams = urllib.urlencode(post_json)
        #conn = httplib.HTTPConnection(host)
        #conn.request("POST", "/task/modify", httpParams, httpHeaders)
        #response = conn.getresponse()
        #print response.read() 
        #如果发送成功则将该stream流对应的位置置为1       
        return (True,"post ok")
        

def test():
    "ud_submit test"
    stream_type_list = ['month','week','day','hour']
    if len(sys.argv) <= 1:
        return (False,"lack argment") 
    if sys.argv[1] not in stream_type_list:
        return (False,"argment wrong\n")
    submit = ud_submit()
    submit.submit_instance(sys.argv[1])
    print 'ran test()'

if __name__ == '__main__':
    test()
