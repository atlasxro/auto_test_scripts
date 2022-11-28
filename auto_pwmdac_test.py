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
cfg_section = "PWMDAC"

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

    begin_info = "**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  pwmdac testing  **********"

    print(begin_info)

    #Please check if PWMDAC is connected
    # is_connected= input("Please check if PWMDAC is connected[y/n]: ")
    is_connected = enable
    while True:
        if is_connected == "y":
            print("Start pwmdac testing.\n")
            break
        elif is_connected == "n":
            is_connected= int(input("Please connect the pwmdac[y/n]: "))
            continue
        else:
            is_connected= int(input("Please enter the correct option[y/n]: "))

    #Gets the current path
    current_directory = os.getcwd()

    # make log dir 
    log_directory_name = r"pwmdac_log/"
    log_gen.mkdir(log_directory_name) 

    # make log file
    log_file_path = log_directory_name+"pwmdac_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
    log_gen.mkfile(log_file_path)

    # open log file, preparing write infomation
    log_file = open(str(log_file_path), "w")

    # write begin_info
    log_file.write(begin_info + "\n")

    # write system info
    sys_info=open(r"/proc/version", "r")
    sys_info_content = sys_info.read()
    log_file.write("System information: " + sys_info_content)
    sys_info.close()

    # write python version
    log_file.write("Python version: " + platform.python_version() + "\n")

    # check the sound card and write information
    log_file.write("Sound card informations:\n")
    sp_aplay = subprocess.Popen("aplay -l", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    aplay_console_lines = sp_aplay.stdout.readlines()
    for i in aplay_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'
        
    # check the ffmpeg information and write information
    log_file.write("ffmpeg informations:\n")
    sp_ffmpeg = subprocess.Popen("ffmpeg -version", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    ffmpeg_console_lines = sp_ffmpeg.stdout.readlines()
    for i in ffmpeg_console_lines:
        print(i.strip().decode("utf-8"))
        log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    # # play the audio information and write information
    # log_file.write("Audio play informations:\n")
    # sp_audio_play = subprocess.Popen("ffmpeg -i audio.wav -f alsa -acodec pcm_s16le hw:0,0", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    # audio_play_console_lines = sp_audio_play.stdout.readlines()
    # for i in audio_play_console_lines:
    #     print(i.strip().decode("utf-8"))
    #     log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

    os.system("ffmpeg -i audio.wav -f alsa -acodec pcm_s16le hw:0,0")

    test_result = input("Whether the audio playback is clear, continuous, and free of noise[y/n]: ")

    while True:
        if test_result == "y":
            test_result_info = "PWMDAC test PASS!"
            is_pass = "y"
            print(test_result_info+"\n")
            log_file.write(test_result)
            break
        elif test_result == "n":
            test_result_info = "PWMDACc test FAIL!\n"
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
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  pwmdac test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("PWMDAC not tested!")
