# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:17:40 2021

@author: lenovo

这个程序负责实现与病人数据库相关的全部内容：
1、接受病人的信息
2、更新病人信息表(information-patient_informaiton)
3、判断病人是否进行体征检测
4、若进行体征检测则创建病人体征数据库(patinet+id)
5、体征数据暂停记录
6、病人出院：停止体征数据检测并删除所有体征数据
7、通过病人的id或姓名信息查询到病人的其他信息
"""

import pymysql
import schedule
import time
import datetime
import random
import re

class NewPatient(object):
    """
    NewPatient类需要实现的功能是：
    在database:patient_information的table:patient_information中插入一行；
    依据编号创建database:patient+id
    """
    def __init__(self,conn):
        self.conn = conn
    #这个函数用于将病人的信息插入表格patient_information中
    def infor_insert(self,name,gender,age,disease,doctor_name,doctor_id,ward_id):
        cursor = self.conn.cursor()
        try:
            switch_sql = "use information"
            cursor.execute(switch_sql)
            insert_sql = "insert into patient_information(name,gender,age,disease,hospitalized_date,doctor_name,doctor_id,ward_id) values('%s','%s','%s','%s','%s','%s','%s','%s') "% (name,gender,age,disease,datetime.date.today(),doctor_name,doctor_id,ward_id)
            cursor.execute(insert_sql)
            print('新病人的信息如下：','姓名：',name,'性别：',gender,'年龄：',age,'疾病：',disease,'入院时间：',datetime.date.today(),'主治医师：',doctor_name,'医师工号：',doctor_id,'病房号：',ward_id)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人信息入库失败")
                self.conn.rollback()
            self.conn.commit()
        finally:
            cursor.close()
    
    """
    def id_receive(self,name):
        cursor = self.conn.cursor()
        try:
            switch_sql = "use information"
            cursor.execute(switch_sql)
            query_sql = "select * from patient_information where name = '%s'" % (name)
            cursor.execute(query_sql)
            results = cursor.fetchone()
            if results is None:
                raise Exception("获取病人id失败") 
            else:
                self.conn.commit()
                return results[0]
        finally:
            cursor.close()
    """
    
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

class DataGeneration(object):
    """
    DataGeneration类应该实现的功能有：
    接受病人数据库编号；
    判断是否需要开始测量生命体征数据；
    若开始测量则检查有无当日的数据库；
    若有当日数据库则向其中添加体征数据；
    若无则新建当日数据库并添加数据；
    随机生成体征数据；
    将体征数据写入以日期为title的table。
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
    #这里的程序还未完成，需要与前端进行对接！用于判断是否开始记录
    def record_judge(self):
        return True
    #这个函数用于判断表格是否存在，存在则返回1，不存在则返回0
    def table_exist(self,table_name):
        show_sql = "show tables"
        cursor = self.conn.cursor()
        cursor.execute(show_sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0
    #这里用于判断table是否已经存在，若存在则向当前table中写入数据
    def table_create(self,database_name):
        cursor = self.conn.cursor()
        timename = 'bio'+str(datetime.date.today()).replace('-', '_')
        try:
            login_sql = "use %s" % (database_name)
            cursor.execute(login_sql)
            if self.table_exist(timename):
                raise Exception("今日表格已经建立，将直接写入数据")
            else:
                create_sql = "create table if not exists %s(time DATETIME NOT NULL,temperature FLOAT(3,1) NOT NULL,systolic INT NOT NULL,diastolic INT NOT NULL,breathe INT NOT NULL,pulse INT NOT NULL)" % (timename)
                cursor.execute(create_sql)
            self.conn.commit()
            return timename
        finally:
            cursor.close()
    #这个函数用于向病人体征数据库patient+id中的体征数据表bio+time写入体征数据
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
            
class DataQuery(object):
    """
    DataQuery类实现的功能：
    通过病人的姓名或id查询病人信息；
    将患者的编号id转化为database_name
    """
    def __init__(self,conn):
        self.conn = conn
    #这个函数用于实现通过病人姓名或id查询病人信息，所的信息将写入一个字典中
    def query(self,title,query_key):
        cursor = self.conn.cursor()
        if title == 'name':
            query_key = '\"%s\"' % (query_key)
        try:
            cursor.execute("use information")
            query_sql = "select * from table patient_information where %s = %s" % (title,query_key)
            cursor.execute(query_sql)
            results = cursor.fetchone()
            if results is None:
                raise Exception("数据库中不存在该患者，请检查输入信息的准确性或患者是否已经出院")
            else:
                self.conn.commit()
                inforlist = {'id','name','gender','age','disease','hospitalized_date','doctor_name','doctor_id','ward_id'}
                infordict = {}
                if len(inforlist) == len(results):
                    for i in range(len(inforlist)):
                        infordict.update({inforlist[i]:results[i]})
                else:
                    raise Exception("信息不匹配")
                return infordict
        finally:
            cursor.close()
    #这个函数用于将病人的id转化为病人数据库名称并返回
    def id_convert(self,patient_id):
        patient_id = str(patient_id)
        if len(patient_id) == 1:
            id_str = '00'+patient_id
        elif len(patient_id) == 2:
            id_str = '0'+patient_id
        else:
            id_str = patient_id
        database_name = "patient"+id_str
        return database_name

class DataDisplay(object):
    """
    DataDisplay类的功能为：
    判断是否需要开始展示体征数据曲线；
    前端提供两大类选择：实时显示和自定义日期显示；
    """

class PatientDischarge(object):
    """
    PatientDischarge类的功能为：
    判断病人是否出院；
    若出院则删除病人所有信息：information-patient_information中的病人行、病人体征数据库patient+id；
    前端弹出送别语；
    """
    def __init__(self,conn):
        self.conn = conn
    #这个函数还没有完成，需要与前端对接：用于判断病人是否出院
    def discharge_judge(self):
        return True
    #这个函数用于删除病人的数据库
    def database_drop(self,database_name):
        cursor = self.conn.cursor()
        try:
            drop_sql = "drop database %s" % (database_name)
            cursor.execute(drop_sql)
            check_sql = "show databases"
            cursor.execute(check_sql)
            results = cursor.fetchone()
            self.conn.commit()
            if results != None:
                raise Exception("删除病人数据库失败")
            else:
                return True
        finally:
            cursor.close()
    #这个函数用于删除病人在patient_information中的信息行
    def line_delete(self,patient_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("use information")
            delete_sql = "delete from patient_information where id = %s" % (patient_id)
            cursor.execute(delete_sql)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人信息删除失败")
                self.conn.rollback()
            self.conn.commit()
        finally:
            cursor.close()
    #这个函数用于删除病人的所有信息
    def information_delete(self,patient_id,database_name):
        PatientDischarge.line_delete(patient_id)
        PatientDischarge.database_drop(database_name)
    #这个函数还没有完成，需要与前端进行对接：用于输出祝福语句
    def say_goodbye(self):
        print("祝您身体健康！")
    
if __name__ == "__main__":
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    newpatient = NewPatient(conn)
    save_data = DataGeneration(conn)
    
    patient_name = "王尼玛"
    patient_age = 35
    patient_gender = "m"
    patient_disease = "抑郁症"
    patient_doctor = {'name':'李博辰','id':'518021911080'}
    patient_ward = 426
    
    def insertdata(name,gender,age,disease,doctor_name,doctor_id,ward_id):
        newpatient.infor_insert(name,gender,age,disease,doctor_name,doctor_id,ward_id)
        
    def receive_id(name):
        return newpatient.id_receive(name)
    
    def createdatabase(id_number):
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
        insertdata(patient_name,patient_gender,patient_age,patient_disease,patient_doctor['name'],patient_doctor['id'],patient_ward)
        database_name = createdatabase(receive_id(patient_name))
        table_name = createtable(database_name)
        schedule.every(5).seconds.do(savedata,database_name,table_name)
    except Exception as e:
        print('出错了：%s'% e)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        