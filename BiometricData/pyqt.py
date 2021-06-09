# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:06:17 2021

@author: lenovo
"""

#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import sys
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import os
import serial
import time
import pexpect
import _thread

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont

present_doctor_id = u'lbc'
present_patient_id = u''
patient_information_changed = 0             #0:new  1:change
fake_present_se1 =0
fake_present_se2 =0
fake_present_se3 =0
fake_present_se4 =0
fake_present_se5 =0
fake_present_se6 =0
speed = 0x64

class DoctorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(448, 155, 1024, 770)
        self.setWindowTitle(u'拆弹部队病人体征监测系统医生端')

        ##初始化下拉菜单
        self.nameList0 = []
        self.nameList0.append('zyt')
        self.nameList0.append('zc')

        self.page1 = QFrame(self)
        self.page1.setVisible(True)
        self.page1.resize(1024, 770)
        self.page2 = QFrame(self)
        self.page2.setVisible(False)
        self.page2.resize(1024, 770)
        self.page3 = QFrame(self)
        self.page3.setVisible(False)
        self.page3.resize(1024, 770)
        self.page4 = QFrame(self)
        self.page4.setVisible(False)
        self.page4.resize(1024, 770)
        self.page5 = QFrame(self)
        self.page5.setVisible(False)
        self.page5.resize(1024, 770)
        self.page6 = QFrame(self)
        self.page6.setVisible(False)
        self.page6.resize(1024, 770)
        self.page7 = QFrame(self)
        self.page7.setVisible(False)
        self.page7.resize(1024, 770)
        self.page8 = QFrame(self)
        self.page8.setVisible(False)
        self.page8.resize(1024, 770)
        self.page9 = QFrame(self)
        self.page9.setVisible(False)
        self.page9.resize(1024, 770)
        self.page10 = QFrame(self)
        self.page10.setVisible(False)
        self.page10.resize(1024, 770)

        self.btntest = QPushButton(self)
        self.btntest.setGeometry(200, 200, 250, 80)
        self.btntest.setText(u'test')
        self.btntest.clicked.connect(self.btntestClicked)

        # page1
        self.bg = QLabel(self.page1)
        self.bg.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg.resize(1024, 770)
        self.bg.setGeometry(0, 0, 1024, 770)

        self.pic1 = QLabel(self.page1)
        self.pic1.setPixmap(QPixmap("./UI_picture/pic1.png"))
        self.pic1.setGeometry(262, 0, 500, 400)

        self.title = QLabel(self.page1)
        self.title.setText(u'欢迎使用拆弹部队病人体征数据监测系统医生端')
        self.title.setFont(QFont("SimHei", 35, QFont.Bold))
        self.title.setGeometry(12, 442, 1000, 80)

        self.input11 = QLineEdit(self.page1)
        self.input11.setGeometry(312, 536, 400, 40)
        self.input11.setPlaceholderText(u'用户名')

        self.input12 = QLineEdit(self.page1)
        self.input12.setGeometry(312, 618, 400, 40)
        self.input12.setPlaceholderText(u'密码')

        self.btn11 = QPushButton(self.page1)
        self.btn11.setGeometry(312, 700, 125, 40)
        self.btn11.setText(u'登录')
        self.btn11.clicked.connect(self.btn11Clicked)

        self.btn12 = QPushButton(self.page1)
        self.btn12.setGeometry(587, 700, 125, 40)
        self.btn12.setText(u'注册')
        self.btn12.clicked.connect(self.btn12Clicked)

        #page2
        self.bg2 = QLabel(self.page2)
        self.bg2.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg2.resize(1024, 770)
        self.bg2.setGeometry(0, 0, 1024, 770)

        self.pic2 = QLabel(self.page2)
        self.pic2.setPixmap(QPixmap("./UI_picture/doctor2.png"))
        self.pic2.setGeometry(85, 100, 300, 350)

        self.txt21 = QLabel(self.page2)
        self.txt21.setText(u'    追求完美的服务,\n做病人的知心朋友')
        self.txt21.setFont(QFont("KaiTi", 28))
        self.txt21.setGeometry(70, 525, 360, 120)

        self.txt22 = QLabel(self.page2)
        self.txt22.setText(u'欢迎注册拆弹部队病人体征数据监测系统')
        self.txt22.setFont(QFont("SimHei", 20, QFont.Bold))
        self.txt22.setGeometry(450, 120, 510, 40)

        self.txt23 = QLabel(self.page2)
        self.txt23.setText(u'用户名')
        self.txt23.setFont(QFont("SimHei", 16, QFont.Bold))
        self.txt23.setGeometry(450, 210, 70, 30)

        self.txt24 = QLabel(self.page2)
        self.txt24.setText(u'密码')
        self.txt24.setFont(QFont("SimHei", 16, QFont.Bold))
        self.txt24.setGeometry(450, 310, 50, 30)

        self.txt25 = QLabel(self.page2)
        self.txt25.setText(u'手机号码')
        self.txt25.setFont(QFont("SimHei", 16, QFont.Bold))
        self.txt25.setGeometry(450, 410, 90, 30)

        self.txt26 = QLabel(self.page2)
        self.txt26.setText(u'验证码')
        self.txt26.setFont(QFont("SimHei", 16, QFont.Bold))
        self.txt26.setGeometry(450, 510, 70, 30)

        self.input21 = QLineEdit(self.page2)
        self.input21.setGeometry(550, 210, 400, 40)
        self.input21.setPlaceholderText(u'用户名')

        self.input22 = QLineEdit(self.page2)
        self.input22.setGeometry(550, 310, 400, 40)
        self.input22.setPlaceholderText(u'密码')

        self.input23 = QLineEdit(self.page2)
        self.input23.setGeometry(550, 410, 400, 40)
        self.input23.setPlaceholderText(u'手机号码')

        self.input24 = QLineEdit(self.page2)
        self.input24.setGeometry(550, 510, 200, 40)
        self.input24.setPlaceholderText(u'验证码')

        self.btn21 = QPushButton(self.page2)
        self.btn21.setGeometry(770, 510, 150, 40)
        self.btn21.setText(u'获取验证码')

        self.btn22 = QPushButton(self.page2)
        self.btn22.setGeometry(550, 610, 150, 40)
        self.btn22.setText(u'注册')
        self.btn22.clicked.connect(self.btn22Clicked)

        #page3
        self.bg3 = QLabel(self.page3)
        self.bg3.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg3.resize(1024, 770)
        self.bg3.setGeometry(0, 0, 1024, 770)

        self.txt31 = QLabel(self.page3)
        self.txt31.setText(u'病人姓名')
        self.txt31.setFont(QFont("SimHei", 15))
        self.txt31.setGeometry(80, 40, 80, 30)

        self.txt32 = QLabel(self.page3)
        self.txt32.setText(u'体征数据')
        self.txt32.setFont(QFont("SimHei", 15))
        self.txt32.setGeometry(80, 110, 80, 30)

        self.btn31 = QPushButton(self.page3)
        self.btn31.setGeometry(80, 200, 125, 40)
        self.btn31.setText(u'查看历史数据')
        self.btn31.clicked.connect(self.btn31Clicked)

        self.btn32 = QPushButton(self.page3)
        self.btn32.setGeometry(80, 340, 125, 40)
        self.btn32.setText(u'联系病人')

        self.btn33 = QPushButton(self.page3)
        self.btn33.setGeometry(80, 480, 125, 80)
        self.btn33.setText(u'紧急事件')

        self.btn34 = QPushButton(self.page3)
        self.btn34.setGeometry(300, 40, 125, 40)
        self.btn34.setText(u'查看病人信息')
        self.btn34.clicked.connect(self.btn34Clicked)

        self.btn35 = QPushButton(self.page3)
        self.btn35.setGeometry(450, 40, 125, 40)
        self.btn35.setText(u'进行机械臂控制')
        self.btn35.clicked.connect(self.btn35Clicked)

        self.btn36 = QPushButton(self.page3)
        self.btn36.setGeometry(600, 40, 125, 40)
        self.btn36.setText(u'编辑个人信息')
        self.btn36.clicked.connect(self.btn36Clicked)

        self.btn37 = QPushButton(self.page3)
        self.btn37.setGeometry(900, 40, 80, 30)
        self.btn37.setText(u'退出')
        self.btn37.clicked.connect(self.btn37Clicked)

        self.cb3 = QComboBox(self.page3)
        self.cb3.setGeometry(170, 40, 90, 30)
        self.cb3.addItems(self.nameList0)
        self.cb3.activated.connect(self.cb3activated)

        self.pic31 = QLabel(self.page3)
        self.pic31.setPixmap(QPixmap("./UI_picture/pic31.jpg"))
        self.pic31.setGeometry(300, 110, 650, 200)

        self.pic32 = QLabel(self.page3)
        self.pic32.setPixmap(QPixmap("./UI_picture/pic32.jpg"))
        self.pic32.setGeometry(300, 340, 650, 400)

        #page4
        self.bg4 = QLabel(self.page4)
        self.bg4.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg4.resize(1024, 770)
        self.bg4.setGeometry(0, 0, 1024, 770)

        self.txt41 = QLabel(self.page4)
        self.txt41.setText(u'机械手控制')
        self.txt41.setFont(QFont("SimHei", 15))
        self.txt41.setGeometry(80, 40, 110, 30)

        self.txt42 = QLabel(self.page4)
        self.txt42.setText(u'紧急停止')
        self.txt42.setFont(QFont("SimHei", 15))
        self.txt42.setGeometry(80, 600, 90, 30)

        self.txt43 = QLabel(self.page4)
        self.txt43.setText(u'体征数据获取')
        self.txt43.setFont(QFont("SimHei", 15))
        self.txt43.setGeometry(80, 145, 130, 30)

        self.txt44 = QLabel(self.page4)
        self.txt44.setText(u'速度档位')
        self.txt44.setFont(QFont("SimHei", 15))
        self.txt44.setGeometry(80, 255, 90, 30)

        self.txt45 = QLabel(self.page4)
        self.txt45.setText(u'微调')
        self.txt45.setFont(QFont("SimHei", 15))
        self.txt45.setGeometry(80, 365, 50, 30)

        self.txt46 = QLabel(self.page4)
        self.txt46.setText(u'实时影像')
        self.txt46.setFont(QFont("SimHei", 15))
        self.txt46.setGeometry(420, 145, 90, 30)

        self.btn41 = QPushButton(self.page4)
        self.btn41.setGeometry(220, 40, 125, 30)
        self.btn41.setText(u'机械手控制说明')
        self.btn41.clicked.connect(self.btn41Clicked)

        self.btn42 = QPushButton(self.page4)
        self.btn42.setGeometry(800, 40, 80, 30)
        self.btn42.setText(u'返回主界面')
        self.btn42.clicked.connect(self.btn42Clicked)

        self.btn43 = QPushButton(self.page4)
        self.btn43.setGeometry(900, 40, 80, 30)
        self.btn43.setText(u'退出')
        self.btn43.clicked.connect(self.btn43Clicked)

        self.btn44 = QPushButton(self.page4)
        self.btn44.setGeometry(40, 90, 80, 30)
        self.btn44.setText(u'启动')
        self.btn44.clicked.connect(self.btn44Clicked)

        self.btn45 = QPushButton(self.page4)
        self.btn45.setGeometry(150, 90, 80, 30)
        self.btn45.setText(u'回原点')
        self.btn45.clicked.connect(self.btn45Clicked)

        self.btn46 = QPushButton(self.page4)
        self.btn46.setGeometry(260, 90, 80, 30)
        self.btn46.setText(u'关闭')
        self.btn46.clicked.connect(self.btn46Clicked)

        self.btn47 = QPushButton(self.page4)
        self.btn47.setGeometry(40, 200, 80, 30)
        self.btn47.setText(u'胸前')
        self.btn47.clicked.connect(self.btn47Clicked)

        self.btn48 = QPushButton(self.page4)
        self.btn48.setGeometry(150, 200, 80, 30)
        self.btn48.setText(u'左臂脉搏')
        self.btn48.clicked.connect(self.btn48Clicked)

        self.btn49 = QPushButton(self.page4)
        self.btn49.setGeometry(260, 200, 80, 30)
        self.btn49.setText(u'右臂脉搏')
        self.btn49.clicked.connect(self.btn49Clicked)

        self.btn410 = QPushButton(self.page4)
        self.btn410.setGeometry(40, 310, 80, 30)
        self.btn410.setText(u'低速')
        self.btn410.clicked.connect(self.btn410Clicked)

        self.btn411 = QPushButton(self.page4)
        self.btn411.setGeometry(150, 310, 80, 30)
        self.btn411.setText(u'中速')
        self.btn411.clicked.connect(self.btn411Clicked)

        self.btn412 = QPushButton(self.page4)
        self.btn412.setGeometry(260, 310, 80, 30)
        self.btn412.setText(u'高速')
        self.btn412.clicked.connect(self.btn412Clicked)

        self.btn413 = QPushButton(self.page4)
        self.btn413.setGeometry(40, 420, 80, 30)
        self.btn413.setText(u'前')
        self.btn413.clicked.connect(self.btn413Clicked)

        self.btn414 = QPushButton(self.page4)
        self.btn414.setGeometry(160, 420, 80, 30)
        self.btn414.setText(u'后')
        self.btn414.clicked.connect(self.btn414Clicked)

        self.btn415 = QPushButton(self.page4)
        self.btn415.setGeometry(40, 480, 80, 30)
        self.btn415.setText(u'左')
        self.btn415.clicked.connect(self.btn415Clicked)

        self.btn416 = QPushButton(self.page4)
        self.btn416.setGeometry(160, 480, 80, 30)
        self.btn416.setText(u'右')
        self.btn416.clicked.connect(self.btn416Clicked)

        self.btn417 = QPushButton(self.page4)
        self.btn417.setGeometry(40, 540, 80, 30)
        self.btn417.setText(u'上')
        self.btn417.clicked.connect(self.btn417Clicked)

        self.btn418 = QPushButton(self.page4)
        self.btn418.setGeometry(160, 540, 80, 30)
        self.btn418.setText(u'下')
        self.btn418.clicked.connect(self.btn418Clicked)

        self.btn419 = QPushButton(self.page4)
        self.btn419.setGeometry(50, 660, 150, 60)
        self.btn419.setText(u'紧急停止')
        self.btn419.clicked.connect(self.btn419Clicked)

        self.pic4 = QLabel(self.page4)
        self.pic4.setPixmap(QPixmap("./UI_picture/pic4.jpg"))
        self.pic4.setGeometry(420, 200, 550, 450)

        #page5
        self.bg5 = QLabel(self.page5)
        self.bg5.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg5.resize(1024, 770)
        self.bg5.setGeometry(0, 0, 1024, 770)

        self.txt51 = QLabel(self.page5)
        self.txt51.setText(u'机械手控制说明')
        self.txt51.setFont(QFont("SimHei", 15))
        self.txt51.setGeometry(80, 40, 150, 30)

        self.btn51 = QPushButton(self.page5)
        self.btn51.setGeometry(800, 40, 80, 30)
        self.btn51.setText(u'返回')
        self.btn51.clicked.connect(self.btn51Clicked)

        self.btn52 = QPushButton(self.page5)
        self.btn52.setGeometry(900, 40, 80, 30)
        self.btn52.setText(u'退出')
        self.btn52.clicked.connect(self.btn52Clicked)

        self.w51 = QWidget(self.page5)
        self.w51.setGeometry(80, 140, 870, 560)
        self.topFiller51 = QWidget(self.w51)
        self.topFiller51.setMinimumSize(870, 2000)
        self.show51 = QLabel(self.topFiller51)
        self.show51.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.show51.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.show51.setText(u'机械手控制说明')
        self.show51.setFont(QFont("SimHei", 15))
        self.show51.setGeometry(0, 0, 850, 2000)
        self.scroll51 = QScrollArea()
        self.scroll51.setWidget(self.topFiller51)
        self.vbox51 = QVBoxLayout()
        self.vbox51.addWidget(self.scroll51)
        self.w51.setLayout(self.vbox51)

        #page6
        self.bg6 = QLabel(self.page6)
        self.bg6.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg6.resize(1024, 770)
        self.bg6.setGeometry(0, 0, 1024, 770)

        self.txt61 = QLabel(self.page6)
        self.txt61.setText(u'姓名')
        self.txt61.setFont(QFont("SimHei", 15))
        self.txt61.setGeometry(80, 40, 50, 30)

        self.txt62 = QLabel(self.page6)
        self.txt62.setText(u'体征信息')
        self.txt62.setFont(QFont("SimHei", 15))
        self.txt62.setGeometry(80, 110, 90, 30)

        self.cb6 = QComboBox(self.page6)
        self.cb6.setGeometry(170, 40, 90, 30)
        self.cb6.addItems(self.nameList0)
        self.cb6.activated.connect(self.cb6activated)

        self.btn61 = QPushButton(self.page6)
        self.btn61.setGeometry(800, 40, 80, 30)
        self.btn61.setText(u'返回主界面')
        self.btn61.clicked.connect(self.btn61Clicked)

        self.btn62 = QPushButton(self.page6)
        self.btn62.setGeometry(900, 40, 80, 30)
        self.btn62.setText(u'退出')
        self.btn62.clicked.connect(self.btn62Clicked)

        #page7
        self.bg7 = QLabel(self.page7)
        self.bg7.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg7.resize(1024, 770)
        self.bg7.setGeometry(0, 0, 1024, 770)

        self.txt71 = QLabel(self.page7)
        self.txt71.setText(u'姓名')
        self.txt71.setFont(QFont("SimHei", 15))
        self.txt71.setGeometry(80, 40, 50, 30)

        self.txt72 = QLabel(self.page7)
        self.txt72.setText(u'病人基本信息')
        self.txt72.setFont(QFont("SimHei", 15))
        self.txt72.setGeometry(80, 110, 130, 30)

        self.cb7 = QComboBox(self.page7)
        self.cb7.setGeometry(170, 40, 90, 30)
        self.cb7.addItems(self.nameList0)
        self.cb7.activated.connect(self.cb7activated)

        self.btn71 = QPushButton(self.page7)
        self.btn71.setGeometry(800, 40, 80, 30)
        self.btn71.setText(u'返回主界面')
        self.btn71.clicked.connect(self.btn71Clicked)

        self.btn72 = QPushButton(self.page7)
        self.btn72.setGeometry(900, 40, 80, 30)
        self.btn72.setText(u'退出')
        self.btn72.clicked.connect(self.btn72Clicked)

        self.btn73 = QPushButton(self.page7)
        self.btn73.setGeometry(300, 40, 125, 40)
        self.btn73.setText(u'添加病人')
        self.btn73.clicked.connect(self.btn73Clicked)

        self.btn74 = QPushButton(self.page7)
        self.btn74.setGeometry(450, 40, 125, 40)
        self.btn74.setText(u'修改病人信息')
        self.btn74.clicked.connect(self.btn74Clicked)

        #page8
        self.bg8 = QLabel(self.page8)
        self.bg8.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg8.resize(1024, 770)
        self.bg8.setGeometry(0, 0, 1024, 770)

        self.txt81 = QLabel(self.page8)
        self.txt81.setText(u'用户名')
        self.txt81.setFont(QFont("SimHei", 15))
        self.txt81.setGeometry(80, 80, 70, 30)

        self.txt82 = QLabel(self.page8)
        self.txt82.setText(u'密码')
        self.txt82.setFont(QFont("SimHei", 15))
        self.txt82.setGeometry(80, 150, 50, 30)

        self.txt83 = QLabel(self.page8)
        self.txt83.setText(u'姓名')
        self.txt83.setFont(QFont("SimHei", 15))
        self.txt83.setGeometry(80, 220, 50, 30)

        self.txt84 = QLabel(self.page8)
        self.txt84.setText(u'性别')
        self.txt84.setFont(QFont("SimHei", 15))
        self.txt84.setGeometry(80, 290, 50, 30)

        self.txt85 = QLabel(self.page8)
        self.txt85.setText(u'出生年月')
        self.txt85.setFont(QFont("SimHei", 15))
        self.txt85.setGeometry(80, 360, 90, 30)

        self.txt86 = QLabel(self.page8)
        self.txt86.setText(u'身份证号码')
        self.txt86.setFont(QFont("SimHei", 15))
        self.txt86.setGeometry(80, 430, 110, 30)

        self.txt87 = QLabel(self.page8)
        self.txt87.setText(u'手机号码')
        self.txt87.setFont(QFont("SimHei", 15))
        self.txt87.setGeometry(80, 500, 90, 30)

        self.txt88 = QLabel(self.page8)
        self.txt88.setText(u'备用号码')
        self.txt88.setFont(QFont("SimHei", 15))
        self.txt88.setGeometry(80, 570, 90, 30)

        self.input81 = QLineEdit(self.page8)
        self.input81.setGeometry(200, 80, 400, 40)
        self.input81.setPlaceholderText(u'用户名')

        self.input82 = QLineEdit(self.page8)
        self.input82.setGeometry(200, 150, 400, 40)
        self.input82.setPlaceholderText(u'密码')

        self.input83 = QLineEdit(self.page8)
        self.input83.setGeometry(200, 220, 400, 40)
        self.input83.setPlaceholderText(u'姓名')

        self.cb8 = QComboBox(self.page8)
        self.cb8.setGeometry(200, 290, 200, 40)
        self.cb8.addItem(u'男')
        self.cb8.addItem(u'女')

        self.input85 = QLineEdit(self.page8)
        self.input85.setGeometry(200, 360, 400, 40)
        self.input85.setPlaceholderText(u'出生年月')

        self.input86 = QLineEdit(self.page8)
        self.input86.setGeometry(200, 430, 400, 40)
        self.input86.setPlaceholderText(u'身份证号码')

        self.input87 = QLineEdit(self.page8)
        self.input87.setGeometry(200, 500, 400, 40)
        self.input87.setPlaceholderText(u'手机号码')

        self.input88 = QLineEdit(self.page8)
        self.input88.setGeometry(200, 570, 400, 40)
        self.input88.setPlaceholderText(u'备用号码')

        self.btn81 = QPushButton(self.page8)
        self.btn81.setGeometry(800, 40, 80, 30)
        self.btn81.setText(u'返回主界面')
        self.btn81.clicked.connect(self.btn81Clicked)

        self.btn82 = QPushButton(self.page8)
        self.btn82.setGeometry(900, 40, 80, 30)
        self.btn82.setText(u'退出')
        self.btn82.clicked.connect(self.btn82Clicked)

        self.btn83 = QPushButton(self.page8)
        self.btn83.setGeometry(200, 640, 125, 40)
        self.btn83.setText(u'保存')
        self.btn83.clicked.connect(self.btn83Clicked)

        self.btn84 = QPushButton(self.page8)
        self.btn84.setGeometry(400, 640, 125, 40)
        self.btn84.setText(u'取消')
        self.btn84.clicked.connect(self.btn84Clicked)

        #page9
        self.bg9 = QLabel(self.page9)
        self.bg9.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg9.resize(1024, 770)
        self.bg9.setGeometry(0, 0, 1024, 770)

        self.txt91 = QLabel(self.page9)
        self.txt91.setText(u'感谢使用拆弹部队病人体\n        征数据监测系统')
        self.txt91.setFont(QFont("SimHei", 35, QFont.Bold))
        self.txt91.setGeometry(237, 304, 550, 160)

        self.btn91 = QPushButton(self.page9)
        self.btn91.setGeometry(400, 640, 125, 40)
        self.btn91.setText(u'退出')
        self.btn91.clicked.connect(self.btn91Clicked)

        #page10
        self.bg10 = QLabel(self.page10)
        self.bg10.setPixmap(QPixmap("./UI_picture/bg.jpg"))
        self.bg10.resize(1024, 770)
        self.bg10.setGeometry(0, 0, 1024, 770)

        self.txt101 = QLabel(self.page10)
        self.txt101.setText(u'姓名')
        self.txt101.setFont(QFont("SimHei", 15))
        self.txt101.setGeometry(80, 80, 50, 30)

        self.txt102 = QLabel(self.page10)
        self.txt102.setText(u'密码')
        self.txt102.setFont(QFont("SimHei", 15))
        self.txt102.setGeometry(80, 150, 50, 30)

        self.txt103 = QLabel(self.page10)
        self.txt103.setText(u'性别')
        self.txt103.setFont(QFont("SimHei", 15))
        self.txt103.setGeometry(80, 220, 50, 30)

        self.txt104 = QLabel(self.page10)
        self.txt104.setText(u'出生年月')
        self.txt104.setFont(QFont("SimHei", 15))
        self.txt104.setGeometry(80, 290, 90, 30)

        self.txt105 = QLabel(self.page10)
        self.txt105.setText(u'身份证号码')
        self.txt105.setFont(QFont("SimHei", 15))
        self.txt105.setGeometry(80, 360, 110, 30)

        self.txt106 = QLabel(self.page10)
        self.txt106.setText(u'手机号码')
        self.txt106.setFont(QFont("SimHei", 15))
        self.txt106.setGeometry(80, 430, 90, 30)

        self.txt107 = QLabel(self.page10)
        self.txt107.setText(u'病症')
        self.txt107.setFont(QFont("SimHei", 15))
        self.txt107.setGeometry(80, 500, 50, 30)

        self.input101 = QLineEdit(self.page10)
        self.input101.setGeometry(200, 80, 400, 40)
        self.input101.setPlaceholderText(u'姓名')

        self.input102 = QLineEdit(self.page10)
        self.input102.setGeometry(200, 150, 400, 40)
        self.input102.setPlaceholderText(u'密码')

        self.cb10 = QComboBox(self.page10)
        self.cb10.setGeometry(200, 220, 200, 40)
        self.cb10.addItem(u'男')
        self.cb10.addItem(u'女')

        self.input104 = QLineEdit(self.page10)
        self.input104.setGeometry(200, 290, 400, 40)
        self.input104.setPlaceholderText(u'出生年月')

        self.input105 = QLineEdit(self.page10)
        self.input105.setGeometry(200, 360, 400, 40)
        self.input105.setPlaceholderText(u'身份证号码')

        self.input106 = QLineEdit(self.page10)
        self.input106.setGeometry(200, 430, 400, 40)
        self.input106.setPlaceholderText(u'手机号码')

        self.input107 = QTextEdit(self.page10)
        self.input107.setGeometry(200, 500, 400, 90)
        self.input107.setPlaceholderText(u'病症')

        self.btn101 = QPushButton(self.page10)
        self.btn101.setGeometry(800, 40, 80, 30)
        self.btn101.setText(u'返回')
        self.btn101.clicked.connect(self.btn101Clicked)

        self.btn102 = QPushButton(self.page10)
        self.btn102.setGeometry(900, 40, 80, 30)
        self.btn102.setText(u'退出')
        self.btn102.clicked.connect(self.btn102Clicked)

        self.btn103 = QPushButton(self.page10)
        self.btn103.setGeometry(200, 640, 125, 40)
        self.btn103.setText(u'保存')
        self.btn103.clicked.connect(self.btn103Clicked)

        self.btn104 = QPushButton(self.page10)
        self.btn104.setGeometry(400, 640, 125, 40)
        self.btn104.setText(u'取消')
        self.btn104.clicked.connect(self.btn104Clicked)

        self.show()

    def btntestClicked(self):
        print('00')

    def btn11Clicked(self):
        global present_doctor_id
        #search_id(self.input11.text())
        if(self.input11.text() != present_doctor_id):
            warn11 = QMessageBox.warning(self, u'warning', u'没有查询到此用户', QMessageBox.Yes, QMessageBox.Yes)
            if warn11 == QMessageBox.Yes:
                self.clear1()
        else:
            if(self.input12.text() == u'123456'):
                self.page1.setVisible(False)
                self.page3.setVisible(True)
                present_doctor_id = self.input11.text()
                self.clear1()
            else:
                warn11 = QMessageBox.warning(self, u'warning', u'密码错误', QMessageBox.Yes, QMessageBox.Yes)
                if warn11 == QMessageBox.Yes:
                    self.clear1()

    def btn12Clicked(self):
        self.page1.setVisible(False)
        self.page2.setVisible(True)
        self.clear1()

    def btn22Clicked(self):
        global present_id
        #write()
        present_id = self.input21.text()
        self.page2.setVisible(False)
        self.page1.setVisible(True)
        self.clear2()

    def btn31Clicked(self):
        self.page3.setVisible(False)
        self.page6.setVisible(True)

    def btn34Clicked(self):
        self.page3.setVisible(False)
        self.page7.setVisible(True)

    def btn35Clicked(self):
        self.page3.setVisible(False)
        self.page4.setVisible(True)

    def btn36Clicked(self):
        self.page3.setVisible(False)
        self.page8.setVisible(True)
        #write      #更新page8

    def btn37Clicked(self):
        self.page3.setVisible(False)
        self.page9.setVisible(True)

    def btn41Clicked(self):
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0A
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1000
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 1000
        fake_present_se6 = 1500

        i = 20
        ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.2)
        while ser.is_open == 1:
            ser.close()
            time.sleep(0.01)
            i = i - 1
            if i == 0:
                i = 20
                warn43 = QMessageBox.warning(self, u'warning', u'串口关闭失败，请检查串口连接', QMessageBox.Yes, QMessageBox.Yes)
                break
        else:
            warn44 = QMessageBox.warning(self, u'warning', u'串口已关闭', QMessageBox.Yes, QMessageBox.Yes)

        self.page4.setVisible(False)
        self.page5.setVisible(True)

    def btn42Clicked(self):
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0A
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1000
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 1000
        fake_present_se6 = 1500

        i = 20
        ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.2)
        while ser.is_open == 1:
            ser.close()
            time.sleep(0.01)
            i = i - 1
            if i == 0:
                i = 20
                warn43 = QMessageBox.warning(self, u'warning', u'串口关闭失败，请检查串口连接', QMessageBox.Yes, QMessageBox.Yes)
                break
        else:
            warn44 = QMessageBox.warning(self, u'warning', u'串口已关闭', QMessageBox.Yes, QMessageBox.Yes)

        self.page4.setVisible(False)
        self.page3.setVisible(True)

    def btn43Clicked(self):
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0A
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1000
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 1000
        fake_present_se6 = 1500

        i = 20
        ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.2)
        while ser.is_open == 1:
            ser.close()
            time.sleep(0.01)
            i = i - 1
            if i == 0:
                i = 20
                warn43 = QMessageBox.warning(self, u'warning', u'串口关闭失败，请检查串口连接', QMessageBox.Yes, QMessageBox.Yes)
                break
        else:
            warn44 = QMessageBox.warning(self, u'warning', u'串口已关闭', QMessageBox.Yes, QMessageBox.Yes)

        self.page4.setVisible(False)
        self.page9.setVisible(True)

    def btn44Clicked(self):         #run
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        ser.open()
        i = 20
        while ser.is_open == 0:
            ser.open()
            time.sleep(0.01)
            i = i - 1
            if i == 0:
                i = 20
                warn42 = QMessageBox.warning(self, u'warning', u'串口开启失败，请检查串口连接', QMessageBox.Yes, QMessageBox.Yes)
                break
        else:
            warn41 = QMessageBox.warning(self, u'warning', u'串口已开启', QMessageBox.Yes, QMessageBox.Yes)
            ser.flushInput()

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0A
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1000
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 1000
        fake_present_se6 = 1500

    def btn45Clicked(self):     #back
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0A
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1000
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 1000
        fake_present_se6 = 1500

    def btn46Clicked(self):     #stop
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0A
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1000
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 1000
        fake_present_se6 = 1500

        i = 20
        while ser.is_open == 1:
            ser.close()
            time.sleep(0.01)
            i = i-1
            if i == 0:
                i = 20
                warn43 = QMessageBox.warning(self, u'warning', u'串口关闭失败，请检查串口连接', QMessageBox.Yes, QMessageBox.Yes)
                break
        else:
            warn44 = QMessageBox.warning(self, u'warning', u'串口已关闭', QMessageBox.Yes, QMessageBox.Yes)

    def btn47Clicked(self):     #xiongqian
        global ser
        global speed
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x0B
        send[4] = 0x0D
        send[5] = speed
        send[6] = 0x00
        ser.write(bytearray(send))

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0D
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1800
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 800
        fake_present_se5 = 2000
        fake_present_se6 = 1500

    def btn48Clicked(self):     #zuobi
        global ser
        global speed
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x0B
        send[4] = 0x0B
        send[5] = speed
        send[6] = 0x00
        ser.write(bytearray(send))

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0B
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1800
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 650
        fake_present_se5 = 1800
        fake_present_se6 = 500

    def btn49Clicked(self):     #youbi
        global ser
        global speed
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x0B
        send[4] = 0x0C
        send[5] = speed
        send[6] = 0x00
        ser.write(bytearray(send))

        send = [0]
        send = send * 7
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x05
        send[3] = 0x06
        send[4] = 0x0C
        send[5] = 0x01
        send[6] = 0x00
        ser.write(bytearray(send))

        fake_present_se1 = 1800
        fake_present_se2 = 1500
        fake_present_se3 = 1500
        fake_present_se4 = 650
        fake_present_se5 = 1800
        fake_present_se6 = 2500

    def btn410Clicked(self):     #speed
        global speed
        speed = 0x32

    def btn411Clicked(self):     #speed
        global speed
        speed = 0x64

    def btn412Clicked(self):     #speed
        global speed
        speed = 0x78

    def btn413Clicked(self):     #qian
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        fake_present_se4 = fake_present_se4 + 40
        fake_present_se5 = fake_present_se5 + 20

        send = [0]
        send = send * 13
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x0B
        send[3] = 0x03
        send[4] = 0x02
        send[5] = 0x10
        send[6] = 0x00
        send[7] = 0x04
        send[8] = fake_present_se4 & 0x00ff
        send[9] = (fake_present_se4 & 0xff00) >> 8
        send[10] = 0x05
        send[11] = fake_present_se5 & 0x00ff
        send[12] = (fake_present_se5 & 0xff00) >> 8
        ser.write(bytearray(send))

    def btn414Clicked(self):     #hou
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        fake_present_se4 = fake_present_se4 - 30
        fake_present_se5 = fake_present_se5 - 20

        send = [0]
        send = send * 13
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x0B
        send[3] = 0x03
        send[4] = 0x02
        send[5] = 0x10
        send[6] = 0x00
        send[7] = 0x04
        send[8] = fake_present_se4 & 0x00ff
        send[9] = (fake_present_se4 & 0xff00) >> 8
        send[10] = 0x05
        send[11] = fake_present_se5 & 0x00ff
        send[12] = (fake_present_se5 & 0xff00) >> 8
        ser.write(bytearray(send))

    def btn415Clicked(self):     #zuo
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        fake_present_se2 = fake_present_se2 - 20
        fake_present_se6 = fake_present_se6 - 20

        send = [0]
        send = send * 13
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x0B
        send[3] = 0x03
        send[4] = 0x02
        send[5] = 0x10
        send[6] = 0x00
        send[7] = 0x02
        send[8] = fake_present_se2 & 0x00ff
        send[9] = (fake_present_se2 & 0xff00) >> 8
        send[10] = 0x06
        send[11] = fake_present_se6 & 0x00ff
        send[12] = (fake_present_se6 & 0xff00) >> 8
        ser.write(bytearray(send))

    def btn416Clicked(self):     #you
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        fake_present_se2 = fake_present_se2 + 20
        fake_present_se6 = fake_present_se6 + 20

        send = [0]
        send = send * 13
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x0B
        send[3] = 0x03
        send[4] = 0x02
        send[5] = 0x10
        send[6] = 0x00
        send[7] = 0x02
        send[8] = fake_present_se2 & 0x00ff
        send[9] = (fake_present_se2 & 0xff00) >> 8
        send[10] = 0x06
        send[11] = fake_present_se6 & 0x00ff
        send[12] = (fake_present_se6 & 0xff00) >> 8
        ser.write(bytearray(send))

    def btn417Clicked(self):     #shang
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        fake_present_se3 = fake_present_se3 - 20
        fake_present_se4 = fake_present_se4 + 20

        send = [0]
        send = send * 13
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x0B
        send[3] = 0x03
        send[4] = 0x02
        send[5] = 0x10
        send[6] = 0x00
        send[7] = 0x03
        send[8] = fake_present_se3 & 0x00ff
        send[9] = (fake_present_se3 & 0xff00) >> 8
        send[10] = 0x04
        send[11] = fake_present_se4 & 0x00ff
        send[12] = (fake_present_se4 & 0xff00) >> 8
        ser.write(bytearray(send))

    def btn418Clicked(self):     #xia
        global ser
        global fake_present_se1
        global fake_present_se2
        global fake_present_se3
        global fake_present_se4
        global fake_present_se5
        global fake_present_se6

        fake_present_se3 = fake_present_se3 + 20
        fake_present_se4 = fake_present_se4 - 20

        send = [0]
        send = send * 13
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x0B
        send[3] = 0x03
        send[4] = 0x02
        send[5] = 0x10
        send[6] = 0x00
        send[7] = 0x03
        send[8] = fake_present_se3 & 0x00ff
        send[9] = (fake_present_se3 & 0xff00) >> 8
        send[10] = 0x04
        send[11] = fake_present_se4 & 0x00ff
        send[12] = (fake_present_se4 & 0xff00) >> 8
        ser.write(bytearray(send))

    def btn419Clicked(self):     #紧急停止
        global ser

        send = [0]
        send = send * 4
        send[0] = 0x55
        send[1] = 0x55
        send[2] = 0x02
        send[3] = 0x07
        ser.write(bytearray(send))

    def btn51Clicked(self):
        self.page5.setVisible(False)
        self.page4.setVisible(True)

    def btn52Clicked(self):
        self.page5.setVisible(False)
        self.page9.setVisible(True)

    def btn61Clicked(self):
        self.page6.setVisible(False)
        self.page3.setVisible(True)

    def btn62Clicked(self):
        self.page6.setVisible(False)
        self.page9.setVisible(True)

    def btn71Clicked(self):
        self.page7.setVisible(False)
        self.page3.setVisible(True)

    def btn72Clicked(self):
        self.page7.setVisible(False)
        self.page9.setVisible(True)

    def btn73Clicked(self):
        global patient_information_changed
        patient_information_changed = 0
        self.page7.setVisible(False)
        self.page10.setVisible(True)

    def btn74Clicked(self):
        global patient_information_changed
        global present_patient_id
        patient_information_changed = 1
        #write      #写入病人原有信息
        self.input101.setText(present_patient_id)
        self.page7.setVisible(False)
        self.page10.setVisible(True)

    def btn81Clicked(self):
        self.page8.setVisible(False)
        self.page3.setVisible(True)
        self.clear8()

    def btn82Clicked(self):
        self.page8.setVisible(False)
        self.page9.setVisible(True)

    def btn83Clicked(self):
        global present_doctor_id
        warn81 = QMessageBox.warning(self, u'warning', u'是否确定保存', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if warn81 == QMessageBox.Yes:
            # write()
            present_doctor_id = self.input81.text()
        else:
            return

    def btn84Clicked(self):
        self.clear8()

    def btn91Clicked(self):
        sys.exit()

    def btn101Clicked(self):
        self.page10.setVisible(False)
        self.page7.setVisible(True)
        self.clear10()

    def btn102Clicked(self):
        self.page10.setVisible(False)
        self.page9.setVisible(True)

    def btn103Clicked(self):
        global present_patient_id
        global patient_information_changed
        if patient_information_changed == 0:
            warn81 = QMessageBox.warning(self, u'warning', u'是否确定保存', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if warn81 == QMessageBox.Yes:
                # write()
                present_patient_id = self.input101.text()
                self.cb3.addItem(self.input101.text())
                self.cb3.setCurrentIndex(self.cb3.count()-1)
                self.cb6.addItem(self.input101.text())
                self.cb6.setCurrentIndex(self.cb6.count()-1)
                self.cb7.addItem(self.input101.text())
                self.cb7.setCurrentIndex(self.cb7.count()-1)
            else:
                return
        else:
            warn82 = QMessageBox.warning(self, u'warning', u'是否确定保存', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if warn82 == QMessageBox.Yes:
                # write_change()
                present_patient_id = self.input101.text()
                self.cb3.setItemText(self.cb3.currentIndex(), self.input101.text())
                self.cb6.setItemText(self.cb6.currentIndex(), self.input101.text())
                self.cb7.setItemText(self.cb7.currentIndex(), self.input101.text())
            else:
                return

    def btn104Clicked(self):
        self.clear10()

    def clear1(self):
        self.input11.setText(u'')
        self.input12.setText(u'')

    def clear2(self):
        self.input21.setText(u'')
        self.input22.setText(u'')
        self.input23.setText(u'')
        self.input24.setText(u'')

    def clear8(self):
        self.input81.setText(u'')
        self.input82.setText(u'')
        self.input83.setText(u'')
        self.cb8.setCurrentIndex(0)
        self.input85.setText(u'')
        self.input86.setText(u'')
        self.input87.setText(u'')
        self.input88.setText(u'')

    def clear10(self):
        self.input101.setText(u'')
        self.input102.setText(u'')
        self.cb10.setCurrentIndex(0)
        self.input104.setText(u'')
        self.input105.setText(u'')
        self.input106.setText(u'')
        self.input107.setText(u'')

    def cb3activated(self):
        global present_patient_id
        present_patient_id = self.cb3.currentText()
        self.cb6.setCurrentIndex(self.cb3.currentIndex())
        self.cb7.setCurrentIndex(self.cb3.currentIndex())
        #showdata()

    def cb6activated(self):
        global present_patient_id
        present_patient_id = self.cb6.currentText()
        self.cb3.setCurrentIndex(self.cb6.currentIndex())
        self.cb7.setCurrentIndex(self.cb6.currentIndex())
        #showdata

    def cb7activated(self):
        global present_patient_id
        present_patient_id = self.cb7.currentText()
        self.cb3.setCurrentIndex(self.cb7.currentIndex())
        self.cb6.setCurrentIndex(self.cb7.currentIndex())

"""
password = 'zyt19991017'
ch = pexpect.spawn('sudo chmod 777 /dev/ttyUSB0')
ch.sendline(password)
print('set password ok')
"""

global ser
#ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    doctorwindow = DoctorWindow()
    doctorwindow.show()
    sys.exit(app.exec_())
