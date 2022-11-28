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
cfg_section = "EMMC"


# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')
emmcdevice = conf.get(cfg_section, 'emmcdevice')
blocksize = conf.get(cfg_section, 'blocksize')
blockcnt = conf.get(cfg_section, 'blockcnt')
expectspeed = conf.get(cfg_section, 'expectspeed')

if enable == "y":
    is_pass = ""
    is_r_pass = ""
    is_w_pass = ""
    
    # 显示开始时间
    begin_time = time.localtime(time.time())

    print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start eMMC test  **********", sep="")

    #获取当前路径
    current_directory = os.getcwd()

    # # open log_all.txt
    # log_file_all = open(current_directory + r"/log_all.txt", "w+")

    #创建对应的日志目录 
    log_directory_name = "emmc_log"
    log_gen.mkdir(log_directory_name)  #调用函数

    #创建日志文件
    log_file_path = str(log_directory_name)+r"/"+"emmc" + "_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
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
    emmc_path = r"/dev/" + emmcdevice
    log_file.write("testing " + emmc_path)
    is_exist_device = os.path.exists(emmc_path)
    # print(is_exist)
    # print(os.path.abspath(os.path.dirname(__file__)))

    # run test
    if is_exist_device:
        # make a temp file to store the results temporary
        tempfile_r_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_r"
        tempfile_r = open(str(tempfile_r_path), 'w')
        tempfile_r.close()
        
        print("eMMC device " + emmcdevice + " exists\n")
        
        # define read command 
        emmc_r_test_command = "time dd if=" + emmc_path + " of=/dev/null bs=" + blocksize + " count=" + blockcnt + " iflag=direct"
        print("Run test:\n" + emmc_r_test_command)
        log_file.write("Run test:\n" + emmc_r_test_command + "\n")
        emmc_r_test_command = emmc_r_test_command + " 2>&1 | tee tempfile_r"
        os.system(emmc_r_test_command)
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
            rmsg = "eMMC READ: PASS  read speed: " + rspeed
            is_r_pass = "y"
            print(rmsg)
            log_file.write(rmsg + "\n")
        else:
            rmsg = "eMMC READ: FAIL  read speed slow: " + rspeed
            is_r_pass = "n"
            print(rmsg)
            log_file.write(rmsg + "\n")

        tempfile_w_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_w"
        tempfile_w = open(str(tempfile_w_path), 'w')
        tempfile_w.close()
            
        # define write command 
        emmc_w_test_command = "time dd if=/dev/zero" + " of=" + emmc_path + " bs=" + blocksize + " count=" + blockcnt
        print("Run test:\n" + emmc_w_test_command)
        log_file.write("Run test:\n" + emmc_w_test_command)
        emmc_w_test_command = emmc_w_test_command + " 2>&1 | tee tempfile_w"
        os.system(emmc_w_test_command)
        w_result = open("tempfile_w", "r")
        w_results = w_result.readlines()
        for i in w_results:
            log_file.write(i.strip() + "\n")
        w_speed_info = w_results[2].strip()
        os.system("rm -f tempfile_w")
        
        # get the read speed
        wspeed = w_speed_info.split(',')[-1].strip()
        wspeed_num = wspeed[0:-4]
        # print(wspeed)

        if wspeed != "" and float(wspeed_num) >= float(expectspeed):
            wmsg = "eMMC WRITE: PASS!  write speed: " + wspeed
            is_w_pass = "y"
            print(wmsg)
            log_file.write(wmsg + "\n")
        else:
            wmsg = "eMMC WRITE: FAIL!  write speed: " + wspeed
            is_w_pass = "n"
            print(wmsg)
            log_file.write(wmsg + "\n")
        
                            
        if is_r_pass == "y" and is_w_pass == "y":
            is_pass = "y"
        else:
            is_pass = "n"
        
    else:
        print("No emmc device exists, please check if the emmc device is installed properly")

    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  eMMC test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("eMMC not tested!")