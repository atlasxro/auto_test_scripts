#!/usr/bin/env python

import os
import time
import platform

import log_gen

# 显示开始时间
begin_time = time.localtime(time.time())

print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start auto test  **********", sep="")

current_path = os.getcwd()

#创建日志文件
log_file_all_path = current_path + r"/" + "log_all" + ".txt"
log_gen.mkfile(log_file_all_path)

log_file_all = open("log_all.txt", "w")

#写入开始时间
log_file_all.write("***************Start test time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',begin_time)) + "***************\n")

#写入系统信息
sys_info=open(r"/proc/version", "r")
sys_info_content = sys_info.read()
log_file_all.write("system information: " + sys_info_content)
sys_info.close()

#写入python版本
log_file_all.write("Python version: " + platform.python_version() + "\n")

# os.system(current_path + r"/auto_gmac_test.py")

# run sd_test
log_file_all.write("*****auto_sd_test*****")
import auto_sd_test
log_file_all.write(auto_sd_test.rmsg + "\n")
log_file_all.write(auto_sd_test.wmsg + "\n")

log_file_all.close