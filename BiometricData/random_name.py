# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 15:02:02 2021

@author: lenovo
"""
import random

def random_patient():
        threedynasties = []
        with open('人名.txt') as f:
            f.seek(0)
            for names in f.readlines():
                names = names.replace(",","").replace("\n","")
                threedynasties.append(names)
            print(threedynasties,'\n')
            print(len(threedynasties))

random_patient()