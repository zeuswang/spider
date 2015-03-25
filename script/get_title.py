#!/usr/bin python

import os
import string
import re
import sys
from chinese import *
def get_title(urlname,str_all):
    if urlname =="banyungong":
        pass
    elif urlname == "gaoqing":
        flist = str_all.split(' ')    
        return flist[2]
#        for f in flist:
#            unicodef = f.decode("utf-8")
#            allchinese = True
#            for uchar in unicodef:
#                if not is_chinese(uchar):
#                    allchinese = False
#            if allchinese:
#                return f

def get_title_year(str_all):
    en_title = ""
    year = ""
    title = ""
    t_list = str_all.split(" ")
    ch2 = t_list
    i = 0
    t = 0
    label = 0
    if "[" in ch2[0]:
        ch1 = str_all.split("]")
        ch2 = ch1[len(ch1)-1].strip().split(" ")
    
    while t < len(t_list):
        ch1 = t_list[t]
        if "." in ch1 and len(ch1.split(".")) > 2:
            ch2 = ch1.split(".")
            label = 1
            break
        t += 1  
    if label == 0 and len(t_list) == 1:
        return title,year

    c1 = ch2[0][0]
    c2 = ch2[0][len(ch2[0])-1]
    if (c1.isalpha() or c1.isdigit()) and (not c2.isalpha() and not c2.isdigit()) :
        i = 1
    
    while i<len(ch2):
        if ch2[i].isdigit() and len(ch2[i]) == 4:
            year = ch2[i]
            break
        elif "-" in ch2[i] and ch2[i].split("-")[0].isdigit() and ch2[i].split("-")[1].isdigit():
            year = ch2[i]
            break
        else:
            en_title += " " + ch2[i]
        i += 1

    en_title2 = ""
    for e in en_title:
        if e.isalpha() or e.isdigit():
            en_title2 += e
        elif e == " ":
            en_title2 += e
            
    title = en_title2.strip()
       
    return title,year

