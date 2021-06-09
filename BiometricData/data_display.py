# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:24:38 2021

@author: lenovo

这个程序负责实现所有和数据显示有关的功能：
1、判断是否要开始展示体征数据曲线；
2、判断实时检测还是自定义日期显示；
3、目前暂定的交互操作：
    下拉菜单（选择显示数据日期）
    复选框（选择需要显示的体征数据）
    滑动条（从左滑动到右为当日全部数据，每日24h的数据均匀分布在滑动条上）
    缩放（鼠标滚轮缩放数据大小）
    悬停提示（悬停至数据点时显示体征值）
4、

【方便查询】bokeh的主要接口：
1、bokeh.models：设置工具条、控制、图形样式属性以及绘图数据等
2、bokeh.layouts：图形显示方式
3、bokeh.palettes：内置调色板
4、bokeh.plotting：figure()命令下基础图形的绘制
5、bokeh.io：图形保存形式
"""
import pymysql
import pandas as pd
import patient
import datetime
from bokeh.plotting import figure
from bokeh.io import output_file, save, show
from bokeh.layouts import gridplot, column
from bokeh.models import HoverTool, ColumnDataSource

class NonRealTime(object):
    """
    NonRealTime类的功能为：
    接受前端对日期的选择
    从数据库中调取选择日期的数据
    显示当前日期的体征数据
    """   
    def __init__(self,conn):
        self.conn = conn
    #这个函数用于将前端输入的字符串日期转化为时间戳格式的日期
    def datetime_convert(self,date):
        show_time = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return show_time
    #这个函数用于将数据从对应数据库中导出为DataFrame格式
    def data_import(self, name, date):
        dataquery = patient.DataQuery(self.conn)
        patient_dict = dataquery.query('name', name)
        id_number = patient_dict['id']
        database_name = dataquery.id_convert(id_number)
        table_name = dataquery.tablename_convert(date)
        cursor = self.conn.cursor()
        login_sql = "use %s" % (database_name)
        cursor.execute(login_sql)
        source_sql = "select * from %s" % (table_name)
        biodata = pd.read_sql(source_sql, self.conn)
        return biodata
    #这个函数用于将DataFrame格式的数据转化为列表
    def frame_to_list(self, biodata, title):
        title = biodata[title].tolist()
        return title
    #这个函数用于生成列表形式的绘图所需数据
    def list_make(self, name, date):
        biodata = self.data_import(name, date)
        #biodata = biodata.set_index(pd.DatetimeIndex(biodata['time']))
        time = biodata['time']
        temp = self.frame_to_list(biodata, 'temperature')
        systolic = self.frame_to_list(biodata, 'systolic')
        diastolic = self.frame_to_list(biodata, 'diastolic')
        breathe = self.frame_to_list(biodata, 'breathe')
        pulse = self.frame_to_list(biodata, 'pulse')
        return time, temp, systolic, diastolic, breathe, pulse
    #这个函数用于生成源形式的绘图所需数据
    def source_make(self, name, date):
        biodata = self.data_import(name, date)
        source = ColumnDataSource(biodata)
        return source
    #这个函数用于以列表作为信息来源画出折线图，可以修改的参数为折线颜色，折线颜色以一字典形式传递
    def list_line_draw(self, linecolor, name, date, time, temp, systolic, diastolic, breathe, pulse):
        temp_title = 'Temperature Data of %s' % (name)
        pressure_title = 'Blodd Pressure Data of %s' % (name)
        breathe_title = 'Breathe Data of %s' % (name)
        pulse_title = 'Pulse Data of %s' % (name)
        x = range(178)
        hover = HoverTool(tooltips=[('index', '$index'), 
                                    ('time', '@time'), 
                                    ('biometric data', '@temperature'),
                                   ])
        TOOLS = ["wheel_zoom, save, pan, reset", hover]
        opt = dict(tools=TOOLS, plot_width=600, plot_height=300)
        #温度绘图
        p_temp = figure(title = temp_title, 
                        x_axis_type = 'datetime', 
                        x_axis_label = 'time', y_axis_label = 'biometric data', 
                        **opt)
        p_temp.line(time, temp, legend_label = 'temperature', line_color = linecolor['temperature'])
        p_temp.circle(time, temp, size=2, color='red', alpha=0.5)
        #血压绘图
        p_pressure = figure(title = pressure_title, 
                            x_axis_type = 'datetime', 
                            x_axis_label = 'time', y_axis_label = 'biometric data', 
                            **opt)
        p_pressure.line(time, systolic, legend_label = 'systolic pressure', line_color = linecolor['systolic'])
        p_pressure.line(time, diastolic, legend_label = 'diastolic pressure', line_color = linecolor['diastolic'])
        #呼吸绘图
        p_breathe = figure(title = breathe_title, 
                           x_axis_type = 'datetime', 
                           x_axis_label = 'time', y_axis_label = 'biometric data', 
                           **opt)
        p_breathe.line(time, breathe, legend_label = 'breathe', line_color = linecolor['breathe'])
        #脉搏绘图
        p_pulse = figure(title = pulse_title, 
                         x_axis_type = 'datetime', 
                         x_axis_label = 'time', y_axis_label = 'biometric data', 
                         **opt)
        p_pulse.line(time, pulse, legend_label = 'pulse', line_color = linecolor['pulse'])
        #矩阵绘图方式
        #s = gridplot([[p_temp, p_pressure], [p_breathe, p_pulse]])
        #列绘图模式
        s = column([p_temp, p_pressure, p_breathe, p_pulse])
        output_name = name + date + '.html'
        output_file(output_name)
        show(s)
    #这个函数用于以源作为信息来源画出折线图，可以修改的参数为折线颜色，折线颜色以一字典形式传递
    def source_line_draw(self, linecolor, name, source):
        temp_title = 'Temperature Data of %s' % (name)
        pressure_title = 'Blodd Pressure Data of %s' % (name)
        breathe_title = 'Breathe Data of %s' % (name)
        pulse_title = 'Pulse Data of %s' % (name)
        hover = HoverTool(tooltips=[('index', '$index'), 
                                    ('time', '@time'), 
                                    ('biometric data', '@temperature'),
                                    ])
        TOOLS = [hover, "wheel_zoom, save, pan, reset"]
        opt = dict(tools=TOOLS, plot_width=300, plot_height=300)
        #温度绘图
        p_temp = figure(title = temp_title, 
                        x_axis_type = 'datetime', 
                        x_axis_label = 'time', y_axis_label = 'biometric data', 
                        **opt)
        p_temp.line(x='time', y='temperature', source=source)
        output_name = name + '.html'
        output_file(output_name)
        show(p_temp)
    

if __name__ == '__main__':
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    nrt_show = NonRealTime(conn)
    name = "张缉"
    date = "2021-06-09"
    #下一段程序使用列表作为信息源
    time, temp, systolic, diastolic, breathe, pulse = nrt_show.list_make(name, date)
    print(time)
    linecolor = {'temperature':'blue', 'systolic':'blue', 'diastolic':'blue', 'breathe':'blue', 'pulse':'blue'}
    nrt_show.list_line_draw(linecolor, name, date, time, temp, systolic, diastolic, breathe, pulse)
    #下一段程序使用源作为信息源
    #source = nrt_show.source_make('刘繇', '2021-06-08')
    #nrt_show.source_line_draw(linecolor, '刘繇', source)
        
    
