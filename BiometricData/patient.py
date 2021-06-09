# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:17:40 2021

@author: lenovo

这个程序负责实现与病人数据库相关的全部内容：
1、接受病人的信息
2、更新病人信息表(information-patient_informaiton)
3、判断病人是否进行体征检测
4、若进行体征检测则创建病人体征数据库(patinet+id)
5、体征数据暂停记录，恢复记录后在原表或新建表中继续记录
6、病人出院：停止体征数据检测并删除所有体征数据
7、通过病人的id或姓名信息查询到病人的其他信息
8、模拟病人信息的测试功能
"""

import pymysql
import schedule
import time
import datetime
import random
import re
import hashlib

class NewPatient(object):
    """
    NewPatient类需要实现的功能是：
    在database:patient_information的table:patient_information中插入一行；
    依据编号创建database:patient+id；
    根据提供的病人姓名和修改信息对现有信息行进行修改
    """
    def __init__(self,conn):
        self.conn = conn
    #这个函数用于将病人的信息插入表格patient_information中
    def infor_insert(self, password, name, gender, age, disease, telephone, NRIC_number, doctor_name, doctor_id, ward_id):
        cursor = self.conn.cursor()
        try:
            switch_sql = "use information"
            cursor.execute(switch_sql)
            insert_sql = "insert into patient_information(password, name, gender, age, disease, telephone, NRIC_number, hospitalized_date, doctor_name, doctor_id, ward_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (password, name, gender, age, disease, telephone, NRIC_number, datetime.date.today(), doctor_name, doctor_id, ward_id)
            cursor.execute(insert_sql)
            print('新病人的信息如下：', '姓名：', name, '性别：', gender, '年龄：', age, '疾病：', disease, '联系方式：', telephone, '身份证号：', NRIC_number, '入院时间：', datetime.date.today(), '主治医师：', doctor_name, '医师工号：', doctor_id, '病房号：', ward_id)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人信息入库失败")
                self.conn.rollback()
            self.conn.commit()
        finally:
            cursor.close()
    #这个函数用于创建病人体征信息数据库，数据库的名称需要从DataQuery类中获得
    def database_create(self,title):
        cursor = self.conn.cursor()
        try:
            sql = "create database %s" % title
            cursor.execute(sql)
            print("病人的体征数据库名字为：",title)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人体征数据建库失败")
                self.conn.rollback()
            else:
                print("病人体征数据库建库成功")
            self.conn.commit()
        finally:
            cursor.close()
    #这个函数用于修改病人在table:patient_information中的信息
    def information_revise(self, name, title, revise_key):
        cursor = self.conn.cursor()
        try:
            cursor.execute("use information")
            revise_sql = "update patient_information set %s = '%s' where name = '%s'" % (title, revise_key, name)
            cursor.execute(revise_sql)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("病人信息修改失败")
                self.conn.rollback()
            else:
                print("病人信息修改成功")
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
    #这里的程序还未完成，需要与前端进行对接！用于判断是否进行记录
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
        inst_tmp = DataQuery(self.conn)
        timename = inst_tmp.tablename_convert(datetime.date.today())
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
    def __init__(self, conn):
        self.conn = conn
    #这个函数用于实现通过病人姓名或id查询病人信息，所的信息将写入一个字典中
    def query(self,title,query_key):
        cursor = self.conn.cursor()
        if title == 'name':
            query_key = '\'%s\'' % (query_key)
        try:
            cursor.execute("use information")
            query_sql = "select * from patient_information where %s = %s" % (title,query_key)
            cursor.execute(query_sql)
            results = cursor.fetchone()
            infordict = {}
            if results is None:
                raise Exception("数据库中不存在该患者，请检查输入信息的准确性或患者是否已经出院")
            else:
                self.conn.commit()
                inforlist = ('id', 'password', 'name', 'gender', 'age', 'disease', 'telephone', 'NRIC_number', 'hospitalized_date', 'doctor_name', 'doctor_id', 'ward_id')
                if len(inforlist) == len(results):
                    for i in range(len(inforlist)):
                        infordict.update({inforlist[i]:results[i]})
                else:
                    raise Exception("信息不匹配")
                return infordict
        finally:
            cursor.close()
    #这个函数用于将病人的id转化为病人数据库名称并返回
    def id_convert(self,id_number):
        id_string = str(id_number)
        if len(id_string) == 1:
            name_str = '00'+id_string
        elif len(id_string) == 2:
            name_str = '0'+id_string
        else:
            name_str = id_string
        database_name = "patient"+name_str
        return database_name
    #这个函数用于将日期转化为表格名，日期格式可为时间格式或字符串格式
    def tablename_convert(self,date):
        if type(date) is not str:
            date_str = str(date)
        else:
            date_str = date
        table_name = 'bio'+date_str.replace('-', '_')
        return table_name
    #这个函数是history函数的辅助函数
    def history_tmp(tables):
        tables = tables[3:]
        tables = tables.replace('_', '-')
        return tables
    #这个函数用于根据病人的姓名获得病人的体征数据记录情况，即哪几天有数据记录
    def history(self,patient_name):
        patient_id = self.query('name', patient_name)['id']
        database_title = self.id_convert(patient_id)
        cursor = self.conn.cursor()
        cursor.execute("use %s") % (database_title)
        cursor.execute("show tables")
        tables = [cursor.fetchall()]
        list_tmp = re.findall('(\'.*?\')',str(tables))
        list_tmp = [re.sub("'",'',each) for each in list_tmp]
        table_list = list(map(self.history_tmp, list_tmp))
        return table_list
    #这个函数用于判断病人名字与密码是否匹配
    def login_judge(self, input_name, input_password):
        try:
            input_dict = self.query('name', input_name)
            if input_password == input_dict['password']:
                print("密码匹配，登陆成功")
                return True
            else:
                print("用户名或密码错误，请重试")
                return False
        except Exception as e:
            print("该病人不存在")
    
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
        return False
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
                raise Exception("病人数据库删除失败")
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
                raise Exception("病人信息行删除失败")
                self.conn.rollback()
            self.conn.commit()
        finally:
            cursor.close()
    #这个函数用于删除病人的所有信息
    def information_delete(self,patient_id,database_name):
        if PatientDischarge.discharge_judge():
            PatientDischarge.line_delete(patient_id)
            PatientDischarge.database_drop(database_name)
        else:
            print("不允许擅自删除病人信息")
    #这个函数还没有完成，需要与前端进行对接：用于输出祝福语句
    def say_goodbye(self):
        print("祝您身体健康！")
    
    
if __name__ == "__main__":
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    newpatient = NewPatient(conn)
    datasave = DataGeneration(conn)
    dataquery = DataQuery(conn)
    goodbye = PatientDischarge(conn)
    #这个函数专门用来随机生成病人信息以进行测试
    def random_name():
        threedynasties = []
        with open('人名.txt') as f:
            f.seek(0)
            for names in f.readlines():
                names = names.replace(",","").replace("\n","")
                threedynasties.append(names)
        return threedynasties[random.randint(0,len(threedynasties))]
    
    def random_gender():
        gender = random.random()
        if gender < 0.5:
            return 'm'
        else:
            return 'f'
    
    def random_password(NRIC_number):
        md5 = hashlib.md5()
        s = "%s" % (NRIC_number)
        md5.update(s.encode())
        md5.hexdigest()
        return md5.hexdigest()
    
    patient_name = "%s" % random_name()
    patient_age = random.randint(1,99)
    patient_gender = random_gender()
    patient_telephone = str(137310)+str(random.randint(11111, 99950))
    patient_NRIC = str(random.randint(111111111111111111, 999999999999999999))
    patient_password = random_password(patient_NRIC)
    patient_disease = "摸鱼症"
    patient_doctor = {'name':'李博辰','id':'518021911080'}
    patient_ward = random.randint(400,500)
    
    try:
        #向patient_information中插入病人信息行
        newpatient.infor_insert(patient_password, patient_name, patient_gender, patient_age, patient_disease, patient_telephone, patient_NRIC, patient_doctor['name'],patient_doctor['id'],patient_ward)
        #查询数据库名称
        infor_dict = dataquery.query('name', patient_name)
        id_number = infor_dict['id']
        database_name = dataquery.id_convert(id_number)
        #创建病人体征数据库
        newpatient.database_create(database_name)
        #创建table并获得table名称
        if datasave.record_judge():
            table_name = datasave.table_create(database_name)
        #测试登陆系统
        test_dict = dataquery.login_judge("孙文", "c1b5babc8b84b6e45f83d6e")
        print(test_dict)
        #测试修改信息
        newpatient.information_revise("韩馥", 'gender', 'f')
        #每5s存储一次数据
        schedule.every(5).seconds.do(datasave.save,database_name,table_name)
    except Exception as e:
        print('出错了：%s'% e)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        