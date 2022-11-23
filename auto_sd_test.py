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
cfg_section = "SD"


# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
sddevice = conf.get(cfg_section, 'sddevice')
# print(sddevice)
blocksize = conf.get(cfg_section, 'blocksize')
blockcnt = conf.get(cfg_section, 'blockcnt')
expectspeed = conf.get(cfg_section, 'expectspeed')

# 显示开始时间
begin_time = time.localtime(time.time())

print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start SD test  **********", sep="")

#获取当前路径
current_directory = os.getcwd()

# # open log_all.txt
# log_file_all = open(current_directory + r"/log_all.txt", "w+")

#创建对应的日志目录 
log_directory_name = "sd_log"
log_gen.mkdir(log_directory_name)  #调用函数

#创建日志文件
log_file_path = str(log_directory_name)+r"/"+"sd" + "_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
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
sd_path = r"/dev/" + sddevice
log_file.write("testing " + sd_path)
# print(sd_path)
is_exist_device = os.path.exists(sd_path)
# print(is_exist)
# print(os.path.abspath(os.path.dirname(__file__)))

# run test
if is_exist_device:
    # make a temp file to store the results temporary
    tempfile_r_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_r"
    tempfile_r = open(str(tempfile_r_path), 'w')
    tempfile_r.close()
    
    print("SD device " + sddevice + " exists\n")
    # tempfile.write("SD device " + sddevice + " exists\n")
    
    # define read command 
    sd_r_test_command = "time dd if=" + sd_path + " of=/dev/null bs=" + blocksize + " count=" + blockcnt + " iflag=direct"
    print("Run test:\n" + sd_r_test_command)
    log_file.write("Run test:\n" + sd_r_test_command + "\n")
    sd_r_test_command = sd_r_test_command + " 2>&1 | tee tempfile_r"
    os.system(sd_r_test_command)
    r_result = open("tempfile_r", "r")
    r_results = r_result.readlines()
    for i in r_results:
        log_file.write(i.strip() + "\n")
    r_speed_info = r_results[2].strip()
    # print(speed_info)
    os.system("rm -f tempfile_r")
    
    # get the read speed
    rspeed = r_speed_info.split(',')[-1].strip()
    rspeed_num = rspeed[0:-4]
    # print(rspeed)
    if rspeed != "" and float(rspeed_num) != 0:
        rmsg = "SD READ: PASS  read speed: " + rspeed
        print(rmsg)
        log_file.write(rmsg + "\n")
    else:
        rmsg = "SD READ: FAIL  read speed slow: " + rspeed
        print(rmsg)
        log_file.write(rmsg + "\n")

        
        
    tempfile_w_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_w"
    tempfile_w = open(str(tempfile_w_path), 'w')
    tempfile_w.close()
        
    # define write command 
    sd_w_test_command = "time dd if=/dev/zero" + " of=" + sd_path + " bs=" + blocksize + " count=" + blockcnt
    print("Run test:\n" + sd_w_test_command)
    log_file.write("Run test:\n" + sd_w_test_command)
    sd_w_test_command = sd_w_test_command + " 2>&1 | tee tempfile_w"
    os.system(sd_w_test_command)
    w_result = open("tempfile_w", "r")
    w_results = w_result.readlines()
    for i in w_results:
        log_file.write(i.strip() + "\n")
    w_speed_info = w_results[2].strip()
    # print(w_speed_info)
    # os.system("rm -f tempfile_w")
    
    # get the read speed
    wspeed = w_speed_info.split(',')[-1].strip()
    wspeed_num = wspeed[0:-4]
    # print(wspeed)

    if wspeed != "" and float(wspeed_num) >= float(expectspeed):
        wmsg = "SD WRITE: PASS  write speed: " + wspeed
        print(wmsg)
        log_file.write(wmsg + "\n")
    else:
        wmsg = "SD WRITE: FAIL  write speed: " + wspeed
        print(wmsg)
        log_file.write(wmsg + "\n")
    
else:
    print("No sd device exists, please check if the sd device is installed properly")
    
# with open(r"./log_all.txt","a") as log_file_all:
#     log_file_all.write("auto_sd_test:\n")
#     log_file_all.write(rmsg + "\n")
#     log_file_all.write(wmsg + "\n")


# 显示结束时间
end_time = time.localtime(time.time())
print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  SD test finish  **********", sep="")

#写入结束时间
log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
log_file.close()
