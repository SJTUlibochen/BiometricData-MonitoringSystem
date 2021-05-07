# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:17:40 2021

@author: lenovo
"""

import pymysql
import schedule
import time
import datetime
import random
import sys

class DataGeneration(object):
    """
    DataGeneration类应该实现的功能有：
    判断前端是否要求开始记录体征数据：若要求开始，则进行以下内容
    接受new_patient.py传递的病人数据库编号；
    在new_patient新创建的数据库patient+number中创建以当前日期为title的table；
    随机生成体征数据；
    将体征数据写入以日期为title的table。
    若没有要求，则不进行任何操作
    """
    def __init__(self,conn):
        self.conn = conn
    #下面若干函数用于模拟体征数据
    #这里模拟体温（36.5-37.5）
    def random_temp(self):
        temperature = round(random.uniform(36.5, 37.5),1)
        return temperature
    #这里模拟收缩压（90-140mmHg）
    def random_sys(self):
        systolic_pressure = random.randint(100, 120)
        return systolic_pressure
    #这里模拟舒张压（60-90mmHg）
    def random_dias(self):
        diastolic_pressure = random.randint(70, 80)
        return diastolic_pressure
    #这里模拟呼吸频率（16-20/min）
    def random_brea(self):
        breathe = random.randint(18, 20)
        return breathe
    #这里模拟脉搏（60-100/min）
    def random_pulse(self):
        pulse = random.randint(80, 90)
        return pulse
    
    def table_create(self,database_name):
        cursor = self.conn.cursor()
        timename = 'bio'+str(datetime.date.today()).replace('-', '_')
        try:
            login_sql = "use %s" % (database_name)
            cursor.execute(login_sql)
            create_sql = "create table %s(time DATETIME NOT NULL,temperature FLOAT(3,1) NOT NULL,systolic INT NOT NULL,diastolic INT NOT NULL,breathe INT NOT NULL,pulse INT NOT NULL)" % (timename)
            cursor.execute(create_sql)
            self.conn.commit()
            return timename
        finally:
            cursor.close()
    
    def save(self,database_name,table_name):
        cursor = self.conn.cursor()
        try:
            login_sql = "use %s" % (database_name)
            cursor.execute(login_sql)
            insert_sql = "insert into %s(time,temperature,systolic,diastolic,breathe,pulse) values('%s','%s','%s','%s','%s','%s')" % (table_name,datetime.datetime.now(),self.random_temp(),self.random_sys(),self.random_dias(),self.random_brea(),self.random_pulse())
            cursor.execute(insert_sql)
            print('写入病人体征数据：',insert_sql)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("体征数据写入失败")
                self.conn.rollback()
            self.conn.commit()
        finally:
            cursor.close()

class NewPatient(object):
    """
    NewPatient类需要实现的功能是：
    在database:patient_information的table:pat_infor中插入一行；
    从数据库中查询患者的编号number；
    依据编号创建database:patient+number
    """
    def __init__(self,conn):
        self.conn = conn
    
    def infor_insert(self,name,gender,age,disease):
        cursor = self.conn.cursor()
        try:
            switch_sql = "use patients_information"
            cursor.execute(switch_sql)
            insert_sql = "insert into pat_infor(name,gender,age,disease,hospitalized_date) values('%s','%s','%s','%s','%s') "% (name,gender,age,disease,datetime.date.today())
            cursor.execute(insert_sql)
            print('新病人的信息如下：','姓名：',name,'性别：',gender,'年龄：',age,'疾病：',disease,'入院时间：',datetime.date.today())
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人信息入库失败")
                self.conn.rollback()
            self.conn.commit()
            
        finally:
            cursor.close()
    
    def database_create(self,title):
        cursor = self.conn.cursor()
        try:
            sql = "create database %s" % title
            cursor.execute(sql)
            print("病人的体征数据库编号为：",title)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人体征数据建库失败")
                self.conn.rollback()
            self.conn.commit()
        finally:
            cursor.close()
    
    def id_receive(self,name):
        cursor = self.conn.cursor()
        try:
            switch_sql = "use patients_information"
            cursor.execute(switch_sql)
            query_sql = "select * from pat_infor where name = '%s'" % (name)
            cursor.execute(query_sql)
            results = cursor.fetchone()
            return results[0]
        finally:
            cursor.close()


if __name__ == "__main__":
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    newpatient = NewPatient(conn)
    save_data = DataGeneration(conn)
    
    patient_name = "朱高煦"
    patient_age = 22
    patient_gender = "m"
    patient_disease = "造反"
    
    def insertdata(name,gender,age,disease):
        newpatient.infor_insert(name,gender,age,disease)
        
    def receive_id(name):
        return newpatient.id_receive(name)
    
    def createdata(id_number):
        if len(str(id_number)) == 1:
            id_str = '00'+str(id_number)
        elif len(str(id_number)) == 2:
            id_str = '0'+str(id_number)
        else:
            id_str = str(id_number)
        patient_id = "patient"+id_str
        newpatient.database_create(patient_id)
        #返回的patient_id为“patient+number”形式
        return patient_id
    
    def createtable(database_name):
        table_name = save_data.table_create(database_name)
        return table_name
    
    def savedata(database_name,table_name):
        save_data.save(database_name,table_name)
    
    try:
        insertdata(patient_name,patient_gender,patient_age,patient_disease)
        database_name = createdata(receive_id(patient_name))
        table_name = createtable(database_name)
        schedule.every(5).seconds.do(savedata,database_name,table_name)
    except Exception as e:
        print('出错了：%s'% e)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        