#!/usr/bin python
# coding=utf8
import os
import string
import re
import sys
from chinese import *
gaoqing_remove_pattern_list = [r'\[.*\]+.*',
                                r'.*[\d]{4}年' ]

banyungong_remove_pattern_list = [r'\[[^\[\]]+\]{1}',
                                r'.*[\d]{4}年' ]

def gaoqing_title(name):
    s = name[:]
    for pattern in gaoqing_remove_pattern_list:

        p = re.compile(pattern) 
        match = p.search(s)
        if match != None:
            tt =  match.group()
            s = s.replace(tt,'')
    return s
def banyungong_title(name):
    s = name[:]
    for pattern in banyungong_remove_pattern_list:

        p = re.compile(pattern) 
        match = p.findall(s)
        for t in match:
    #        print t
            s = s.replace(t,'')
    #        print s
    if "." in s:
        pattern = re.compile(r'([a-zA-Z0-9\.]+[0-9]{4}\.)') 
        match = pattern.findall(s)
        if len(match)>0:
            tt =  match[-1]
            return tt[0:(len(tt) -6)]
    else:
        pattern = re.compile(r'([\w\d\s]+)[0-9]{4}\s') 
        match = pattern.findall(s)
        if len(match)>0:
            tt =  match[-1]
            return tt

    return s


def get_title(urlname,str_all):
    if "合集" in str_all:
        return None
    if "banyungong" in urlname:
        return banyungong_title(str_all)
    elif  "gaoqing" in urlname:
        return gaoqing_title(str_all)

if __name__=="__main__":
    print get_title("http://gaoqing.la/","2014年 超能陆战队 大英雄联盟 大英雄天团 [漫威同名漫画改编 冰雪奇缘原班人马制作] 03-01 1080P超清 , 3D高清 , 720P高清 , Bluray蓝光原盘")
    print get_title("http://banyungong/","lang超能陆战队 abc dddd ssss 2015 1080p")
    print get_title("http://banyungong/","[至暴之年 / 暴力年代(台) / 最暴烈的一年(港)「最坏的时代 最好的人」] A.Most.Violent.Year.2014.1080p.BluRay.x264.DTS-WiKi 11.04 GB")
    print get_title("http://banyungong/","[日本] [喜剧] 2014年 圆桌 [致所有从小学三年级走过的大人们]")
