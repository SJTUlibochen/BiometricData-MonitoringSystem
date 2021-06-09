# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:17:07 2021

@author: lenovo
"""

import pandas as pd
import pymysql
from bokeh.io import curdoc, output_file
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper, Slider
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row
#import schedule
#import time

if __name__ == '__main__':
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    cursor = conn.cursor()
    login_sql = "use patient017"
    cursor.execute(login_sql)
    act_sql = "select * from bio2021_06_08"
    biodata = pd.read_sql_query(act_sql, conn)
    print(biodata)
    
    output_file("bokeh_test.html")
    source = ColumnDataSource(data = {'x':biodata.time, 'y':biodata.temperature})
    plot = figure(title = "温度体征数据显示测试", 
                  plot_height = 600, plot_width=1000, 
                  )
    plot.circle(x='x', y='y', fill_alpha=0.8, source=source)
    show(figure)
    
    
    