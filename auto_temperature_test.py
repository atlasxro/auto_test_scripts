#!/usr/bin/env python
# -*- coding: UTF-8 -*- 

import os
import time
import sys
import platform
import subprocess
import configparser

import log_gen

# define cfg_name
cfg_name = "cfg.ini"
# indicates the location section of configuration in cfg_section
cfg_section = "TEMPERATURE"


# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')

if enable == "y":
    is_pass = ""
    
    # 显示开始时间
    begin_time = time.localtime(time.time())

    print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start temperature test  **********", sep="")

    #获取当前路径
    current_directory = os.getcwd()

    # # open log_all.txt
    # log_file_all = open(current_directory + r"/log_all.txt", "w+")

    #创建对应的日志目录 
    log_directory_name = "temperature_log"
    log_gen.mkdir(log_directory_name)  #调用函数

    #创建日志文件
    log_file_path = str(log_directory_name)+r"/"+"temperature" + "_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
    log_gen.mkfile(log_file_path)

    #打开日志文件，准备向其中写入信息
    log_file = open(str(log_file_path), "w")

    #写入开始时间
    log_file.write("***************Start test time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',begin_time)) + "***************\n")

    #写入系统信息
    sys_info=open(r"/proc/version", "r")
    sys_info_content = sys_info.read()
    log_file.write("system information: " + sys_info_content)
    sys_info.close()

    #写入python版本
    log_file.write("Python version: " + platform.python_version() + "\n")

    # determine if the device exists
    temp_driver = "/sys/class/hwmon/hwmon0/temp1_input"
    
    is_exists = os.path.exists(temp_driver)
    
    if is_exists:
        temp_command = "cat " +  temp_driver
        sp = subprocess.Popen(temp_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        temperature = sp.stdout.readline().strip().decode("utf-8")
        temp_msg = "Temperature driver is exist, test PASS! value=" + temperature
        is_pass = "y"
        print(temp_msg)
        log_file.write(temp_msg)
    else:
        temp_msg = "Temperature driver " + temp_driver + " does not exist, test FAIL!"
        is_pass = "n"
        print(temp_msg)
        log_file.write(temp_msg)
        
    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  Temperature test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("Temperature not tested!")