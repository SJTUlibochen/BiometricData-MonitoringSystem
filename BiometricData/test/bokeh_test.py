import pandas as pd
from bokeh.plotting import figure, output_file, show, save
import pymysql
import datetime

if __name__=='__main__':
    conn = pymysql.connect(host = "localhost",user = "root",password = "SJTUlbc2000101",charset = "utf8")
    cursor = conn.cursor()
    cursor.execute("use patient022")
    source_sql = "select * from bio2021_06_08"
    data = pd.read_sql(source_sql, conn)
    biodata_title = ['time', 'temperature', 'systolic', 'diastolic', 'breathe', 'pulse']
    """
    time = data['time'].tolist()
    temp = data['temperature'].tolist()
    systolic = data['systolic'].tolist()
    diastolic = data['diastolic'].tolist()
    breathe = data['breathe'].tolist()
    pulse = data['pulse'].tolist()
    """
    def frametolist(biodata, titles):
       titles = biodata[titles].tolist()
       return titles
    time = frametolist(data, 'time')
    temp = frametolist(data,'temperature')
    systolic = frametolist(data,'systolic')
    
    x = range(178)
    p = figure(title='fisrt real data test', 
               x_axis_label='int', y_axis_label='biometric data', 
               width=700, height=350)
    p.line(x, temp, legend='temperature', line_color='black')
    p.line(x, systolic, legend='systolic', line_color='navy')
    
    output_file('test4.html')
    show(p)