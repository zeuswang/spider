#!/usr/bin python
# coding=utf8
import os
import string
import re
import sys
from chinese import *
gaoqing_remove_pattern_list = [r'\[.*\]+.*',
                                r'.*[\d]{4}年' ]
def gaoqing_title(name):
    s = name[:]
    for pattern in gaoqing_remove_pattern_list:

        p = re.compile(pattern) 
        match = p.search(name)
        if match != None:
            tt =  match.group()
            s = s.replace(tt,'')
    return s

def get_title(urlname,str_all):
    if "合集" in str_all:
        return None
    if "banyungong" in urlname:
        if "." in str_all:
            pattern = re.compile(r'([a-zA-Z0-9\.]+[0-9]{4}\.)') 
            match = pattern.search(str_all)
            if match != None:
                tt =  match.group()
                return tt[0:(len(tt) -6)]
           
        return str_all
    elif  "gaoqing" in urlname:
        return gaoqing_title(str_all)
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
print get_title("http://gaoqing.la/","2014年 超能陆战队 大英雄联盟 大英雄天团 [漫威同名漫画改编 冰雪奇缘原班人马制作] 03-01 1080P超清 , 3D高清 , 720P高清 , Bluray蓝光原盘")
