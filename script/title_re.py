#/usr/bin python

import os
import string
import re
import sys

def get_title_year(str_all):
    
    delete_pattern = []
    get_pattern = []
    title = ""
    year = ""

    p_brackets = re.compile(r'(\[.*\]|\([^(\(|\))]*\))')
    delete_pattern.append(p_brackets)
    
    p_name_year = re.compile(r'(\.|\s)+[(\d|\w)*(\s|\.)]{1,}((\d){4}|(\d){4}-(\d){4})(\.|\s)')
    get_pattern.append(p_name_year)
    
    p_chinese = re.compile(r'[^(\d|\w|\.|\s)]+[\d\.]*')
    delete_pattern.append(p_chinese)
    
    p_year = re.compile(r'(\.|\s)((\d){4}|(\d){4}-(\d){4})(\.|\s)')
    delete_pattern.append(p_year)
 #   print str_all
    str2 = p_brackets.sub(' ',str_all) 
#    print str2
    str3 = p_chinese.sub(' ^$ ',str2)
#    print str3    
   
    t = p_name_year.search(str3)
    if t:
        en =t.group()
#        print en
        y_match = p_year.search(en)
        if y_match:
            year = y_match.group().replace(".","").strip()
        en2 = p_year.sub('',en)
        title = en2.replace("."," ").strip()
    return title,year

