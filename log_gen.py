#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

def mkdir(path): #自定义日志文件夹创建函数
    folder = os.path.exists(path)
    if not folder:  #判断是否存在文件夹如果不存在则创建为文件夹
        print("---  创建新的日志文件夹",  path, "  ---", sep="")
        os.makedirs(path)  #makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  OK  ---")
    else:
        print("---  日志文件夹", path, "已存在!  ---", sep="")
        
def mkfile(file):  #自定义创建文件函数
    is_log_file = os.path.exists(file)
    if not is_log_file:
        print("---  创建新的日志文件：", file, "  ---", sep="")
        logfile = open(file, 'w')
        print("---  OK  ---")
        logfile.close()
    else:
        print("---  日志文件：", file, "已存在!  ---", sep="")