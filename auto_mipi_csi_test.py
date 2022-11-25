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
cfg_section = "CSI"

# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')

if enable == "y":
    # get begin time
    begin_time = time.localtime(time.time())

    begin_info = "**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  mipi-csi testing  **********"

    print(begin_info)

    #Please check if PWMDAC is connected
    # is_connected= input("Please check if the mipi-csi and hdmi are connected[y/n]: ")
    is_connected = enable
    while True:
        if is_connected == "y":
            print("Start mipi-csi testing.\n")
            break
        elif is_connected == "n":
            is_connected= int(input("Please connect the mipi-csi[y/n]: "))
            continue
        else:
            is_connected= int(input("Please enter the correct option[y/n]: "))

    #Gets the current path
    current_directory = os.getcwd()

    # make log dir 
    log_directory_name = r"mipi-csi_log/"
    log_gen.mkdir(log_directory_name) 

    # make log file
    log_file_path = log_directory_name+"mipi-csi_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
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

    # build pipeline
    log_file.write("*****start pipeline:\n")
    sp_pipeline_start = subprocess.Popen("media-ctl-pipeline.sh -d /dev/media0 -i csiphy0 -s ISP0 -a start", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    pipeline_start_console_lines = sp_pipeline_start.stdout.readlines()
    for i in pipeline_start_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    # is_pipeline = sp_pipeline_start.poll()
    # while True:
    #     if is_pipeline == True:
    #         break
    #     else:
    #         print("cannot start pipeline, test fail")
    #         log_file.write("Test fail, cannot start the pipeline")
    #         log_file.close()

    # check the mipi-csi, then write information 
    log_file.write("*****sensor parameters:\n")
    sp_sensor_para = subprocess.Popen("v4l2-ctl -d /dev/video1 -L", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    sensor_para_console_lines = sp_sensor_para.stdout.readlines()
    for i in sensor_para_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    log_file.write("*****sensor list formats:\n")
    sp_sensor_format = subprocess.Popen("v4l2-ctl -d /dev/video1 --list-formats", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    sensor_format_console_lines = sp_sensor_format.stdout.readlines()
    for i in sensor_format_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'
        
    # isp_command = "cd /root/ISP && ./stf_isp_ctrl"
    # log_file.write("start isp control:\n")
    # os.system(isp_command)
    # sp_isp_command = subprocess.Popen(isp_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    
    def terminate_func(thread_ter, stoptime):
        time.sleep(stoptime)
        thread_ter.terminate()
        
    v4l2_command = "v4l2test -d /dev/video1 -f 5 -c -C 0 -W 1920 -H 1080 -m 0 -t 2"
    # os.system(v4l2_command)

    sp_v4l2_command = subprocess.Popen("exec " + v4l2_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    # time.sleep(10)
    # sp_v4l2_command.terminate()
    terminate_func(sp_v4l2_command, 10)
    time.sleep(1)
    # sp_isp_command.kill()
    # time.sleep(1)

    # stop pipeline
    # log_file = open(str(log_file_path), "w")
    log_file.write("*****stop pipeline:\n")
    sp_pipeline_stop = subprocess.Popen("media-ctl-pipeline.sh -d /dev/media0 -i csiphy0 -s ISP0 -a stop", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    pipeline_stop_console_lines = sp_pipeline_stop.stdout.readlines()
    for i in pipeline_stop_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    test_result = input("Whether the video playback is clear and continuous[y/n]: ")

    while True:
        if test_result == "y":
            test_result_info = "mipi-csi test successful!"
            print(test_result_info+"\n")
            log_file.write("*****test_result: " + test_result_info)
            break
        elif test_result == "n":
            test_result_info = "mipi-csi test fail!\n"
            note_information = input("Please describe the phenomenon that occurred during the test: ")
            print(test_result_info+"\n")
            log_file.write("*****test result: " + test_result_info + "\n")
            log_file.write("*****Note informations: " + note_information)
            break
        else:
            test_result = input("Please enter the correct options[y/n]: ")
            continue

    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  mipi-csi test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("CSI not tested!")
 