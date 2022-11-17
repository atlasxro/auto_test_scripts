#!/usr/bin/env python

# -*- coding: UTF-8 -*- 

import os
import time
import sys
import platform
import socket
import subprocess

import log_gen

# get begin time
begin_time = time.localtime(time.time())

print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start the pwmdac test  **********", sep="")

#Please check if PWMDAC is connected
is_connected= int(input("Please check if PWMDAC is connected[y/n]: "))
while True:
    if is_connected:
        print("测试gmac_",gmac_num,sep="")
        break
    else:
        gmac_num = int(input("请输入正确的gmac端口编号[0/1]: "))
        continue

#获取当前路径
current_directory = os.getcwd()

#创建对应gmac的日志目录 
log_directory_name = "gmac_log"+r"/gmac_"+str(gmac_num)
log_gen.mkdir(log_directory_name)  #调用函数

#创建日志文件
log_file_path = str(log_directory_name)+r"/"+"gmac"+str(gmac_num)+"_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
log_gen.mkfile(log_file_path)

#打开日志文件，准备向其中写入信息
log_file = open(str(log_file_path), "w")

#写入开始时间
log_file.write("***************开始测试时间: " + str(time.strftime('%y-%m-%d_%H:%M:%S',begin_time)) + "***************\n")

#写入系统信息
sys_info=open(r"/proc/version", "r")
sys_info_content = sys_info.read()
log_file.write("系统信息: " + sys_info_content)
sys_info.close()

#写入python版本
log_file.write("Python版本: " + platform.python_version() + "\n")






os.system("ffmpeg -i audio.wav -f alsa -acodec pcm_s16le hw:0,0", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)