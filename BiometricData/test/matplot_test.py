# -*- coding: utf-8 -*-
"""
Created on Fri May  7 10:13:12 2021

@author: lenovo
"""

import matplotlib.pyplot as plt
import numpy as np
import time

plt.suptitle("Plot by pyplot API scrpt")
t = np.linspace(0, 10, 40)
y1 = np.sin(t)
y2 = np.cos(t*2)
plt.subplot(1, 2, 1)
plt.plot(t,y1,'r-o',label = 'sin', linewidth=1, markersize = 5)
plt.plot(t,y2,'b:',label = 'cos', linewidth=2)
plt.xlabel('time(sec)')
plt.ylabel('value')
plt.title("plot of functions")
plt.xlim([0, 10])
plt.ylim([-2, 2])
plt.legend()
plt.show()
