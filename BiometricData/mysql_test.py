# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:21:53 2021

@author: lenovo
"""

import pymysql
import re

if __name__ == "__main__":
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    cursor = conn.cursor()
    try:
        switch_sql = 'use patient_test'
        login_sql = 'use information'
        #cursor.execute(switch_sql)
        cursor.execute(login_sql)
        #query_sql = "select * from patient_information where name = '徐阶'"
        #query_sql = "select * from patient_information where name = '李博辰'"
        #cursor.execute(query_sql)
        """
        results = cursor.fetchone()
        if results is not None:
            inforlist = ['id','name','gender','age','disease','hospitalized_date','doctor_name','doctor_id','ward_id']
            infordict = {}
            i = 1
            for i in range(len(inforlist)):
                infordict.update({inforlist[i]:results[i]})
            print(infordict,'\n')            
        else:
            print('1')
        """
        title = 'name'
        query_key = '徐阶'
        if title == 'name':
            print(query_key,'\n')
            query_key = '\"%s\"' % (query_key)
            print(query_key)
        query_sql = "select * from patient_information where %s = %s" % (title,query_key)
        print(query_sql,'\n')
        cursor.execute(query_sql)
        results = cursor.fetchone()
        print(results)
        #create_sql = "create table if not exists bio20001004(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)"
        #cursor.execute(create_sql)
        #show_sql = "show tables"
        #cursor.execute(show_sql)
        #while (cursor.fetchone()!= None):
            #print(cursor.fetchone())
        #tables = [cursor.fetchall()]
        #print(tables,'\n')
        #table_list = re.findall('(\',.*?\')',str(tables))
        conn.commit()
    finally:
        cursor.close()