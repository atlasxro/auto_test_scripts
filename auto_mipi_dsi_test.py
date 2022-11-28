#!/usr/bin/env python

# -*- coding: UTF-8 -*- 

import os
import time
import sys
import platform
import socket
import subprocess
import configparser

import log_gen

# define cfg_name
cfg_name = "cfg.ini"
# indicates the location section of configuration in cfg_section
cfg_section = "DSI"

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

    begin_info = "**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  mipi_dsi testing  **********"

    print(begin_info)

    # 2-lane or 4-lane
    # mipi2or4 = input("2_lane or 4_lane mipi screen[2/4]: ")
    mipi2or4 = conf.get(cfg_section, 'lane')
    while True:
        if int(mipi2or4) == 2:
            log_info = "*****Testing the 2_lane mipi screen.*****\n"
            print(log_info)
            break
        elif int(mipi2or4) == 4:
            log_info = "*****Testing the 4_lane mipi screen.*****\n"
            print(log_info)
            break
        else:
            mipi2or4 = input("Please enter a correct option[2/4]: ")
            continue

    #Gets the current path
    current_directory = os.getcwd()

    # make log dir 
    log_directory_name = r"mipi_dsi_log/" + mipi2or4 + r"_lane_mipi/"
    log_gen.mkdir(log_directory_name) 

    # make log file
    log_file_path = log_directory_name+"mipi_dsi_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
    log_gen.mkfile(log_file_path)

    # open log file, preparing write infomation
    log_file = open(str(log_file_path), "w")

    # write begin_info
    log_file.write(begin_info + "\n")

    log_file.write(log_info)

    #Please check if mipi-dsi is connected
    # is_connected= input("Please check if the mipi_dsi is connected[y/n]: ")
    is_connected = enable
    while True:
        if is_connected == "y":
            print("Start mipi_dsi testing.\n")
            break
        elif is_connected == "n":
            is_connected= int(input("Please connect the mipi_dsi[y/n]: "))
            continue
        else:
            is_connected= int(input("Please enter the correct option[y/n]: "))


    # write system info
    sys_info=open(r"/proc/version", "r")
    sys_info_content = sys_info.read()
    log_file.write("*****System information: " + sys_info_content)
    sys_info.close()

    # write python version
    log_file.write("*****Python version: " + platform.python_version() + "\n")

    def terminate_func(thread_ter, stoptime):
        time.sleep(stoptime)
        thread_ter.terminate()

    # check the mipi-dsi, then write information  
    log_file.write("*****mipi_dsi informations:\n")
    sp_mipi_dsi = subprocess.Popen("modeprint starfive", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    mipi_dsi_console_lines = sp_mipi_dsi.stdout.readlines()
    for i in mipi_dsi_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    if int(mipi2or4) == 2:
        mipi_dsi_command = "modetest -M starfive -a -s 118@35:800x480 -P 74@35:800x480 -F tiles"
    else:
        mipi_dsi_command = "modetest -M starfive -a -s 118@35:800x1280 -P 74@35:800x1280 -F tiles"
        
    sp_mipi_dsi_command = subprocess.Popen("exec " + mipi_dsi_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    # time.sleep(5)
    # sp_mipi_dsi_command.terminate()
    terminate_func(sp_mipi_dsi_command,10)
    time.sleep(1)


    test_result = input("Whether the tiles playback is clear?[y/n]: ")

    while True:
        if test_result == "y":
            test_result_info = "MIPI-DSI test PASS!"
            is_pass = "y"
            print(test_result_info+"\n")
            log_file.write(test_result_info)
            break
        elif test_result == "n":
            test_result_info = "MIPI-DSI test FAIL!"
            note_information = input("Please describe the phenomenon that occurred during the test: ")
            is_pass = "n"
            print(test_result_info+"\n")
            log_file.write("Note informations: " + test_result_info)
            log_file.write(note_information)
            break
        else:
            test_result = input("Please enter the correct options[y/n]: ")
            continue

    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  mipi_dsi test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("DSI not tested!")

 