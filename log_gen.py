#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

def mkdir(path): #自定义日志文件夹创建函数
    folder = os.path.exists(path)
    if not folder:  #判断是否存在文件夹如果不存在则创建为文件夹
        print("---  Create new log folder: ",  path, "  ---", sep="")
        os.makedirs(path)  #makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  OK  ---")
    else:
        print("---  log folder: ", path, "exists!  ---", sep="")
        
def mkfile(file):  #自定义创建文件函数
    is_log_file = os.path.exists(file)
    if not is_log_file:
        print("---  Create new log file: ", file, "  ---", sep="")
        logfile = open(file, 'w')
        print("---  OK  ---")
        logfile.close()
    else:
        print("---  log file: ", file, "exists!  ---", sep="")