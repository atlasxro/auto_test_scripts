#!/usr/bin/env python

# -*- coding: UTF-8 -*- 

import os
import time
import platform
import subprocess
import configparser

import log_gen

# define cfg_name
cfg_name = "cfg.ini"
# indicates the location section of configuration in cfg_section
cfg_section = "UVC"

# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')

if enable == "y":
    is_pass = ""
    
    # get begin time
    begin_time = time.localtime(time.time())

    begin_info = "**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  uvc testing  **********"

    print(begin_info)

    #Gets the current path
    current_directory = os.getcwd()

    # make log dir 
    log_directory_name = r"uvc_log/"
    log_gen.mkdir(log_directory_name) 

    # make log file
    log_file_path = log_directory_name+"uvc_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
    log_gen.mkfile(log_file_path)

    # open log file, preparing write infomation
    log_file = open(str(log_file_path), "w")

    # write begin_info
    log_file.write(begin_info + "\n")

    # write system info
    sys_info=open(r"/proc/version", "r")
    sys_info_content = sys_info.read()
    log_file.write("*****System information: " + sys_info_content)
    sys_info.close()

    # write python version
    log_file.write("*****Python version: " + platform.python_version() + "\n")

    # check the uvc, then write information 
    log_file.write("*****sensor parameters:\n")
    sp_sensor_para = subprocess.Popen("v4l2-ctl -d /dev/video4 -L", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    sensor_para_console_lines = sp_sensor_para.stdout.readlines()
    for i in sensor_para_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    log_file.write("*****sensor list formats:\n")
    sp_sensor_format = subprocess.Popen("v4l2-ctl -d /dev/video4 --list-formats", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    sensor_format_console_lines = sp_sensor_format.stdout.readlines()
    for i in sensor_format_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    v4l2_command = "v4l2test -d /dev/video4 -f 3 -c -C 0 -W 1920 -H 1080 -m 0 -t 2"
    # os.system(v4l2_command)

    sp_v4l2_command = subprocess.Popen("exec " + v4l2_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    time.sleep(10)
    sp_v4l2_command.terminate()
    time.sleep(1)

    test_result = input("Whether the video playback is clear and continuous[y/n]: ")

    while True:
        if test_result == "y":
            test_result_info = "UVC test PASS!"
            is_pass = "y"
            print(test_result_info+"\n")
            log_file.write("*****test_result: " + test_result_info)
            break
        elif test_result == "n":
            test_result_info = "UVC test FAIL!\n"
            note_information = input("Please describe the phenomenon that occurred during the test: ")
            is_pass = "n"
            print(test_result_info+"\n")
            log_file.write("*****test result: " + test_result_info + "\n")
            log_file.write("*****Note informations: " + note_information)
            break
        else:
            test_result = input("Please enter the correct options[y/n]: ")
            continue

    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  uvc test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("UVC not tested!")
