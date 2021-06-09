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
    def function_tmp(tables):
        tables = tables[3:]
        tables = tables.replace('0', '9')
        return tables
    try:
        switch_sql = 'use patient_test'
        cursor.execute(switch_sql)
        show_sql = "show tables"
        cursor.execute(show_sql)
        tables = [cursor.fetchall()]
        print(tables,'\n')
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        print(table_list,'\n')
        test = list(map(function_tmp, table_list))
        print(test)
        conn.commit()
    finally:
        cursor.close()