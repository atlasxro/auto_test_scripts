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

begin_info = "**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  hdmi testing  **********"

print(begin_info)

#Please check if PWMDAC is connected
is_connected= input("Please check if the HDMI and earphone are connected[y/n]: ")
while True:
    if is_connected == "y":
        print("Start HDMI testing.\n")
        break
    elif is_connected == "n":
        is_connected= int(input("Please connect the HDMI[y/n]: "))
        continue
    else:
        is_connected= int(input("Please enter the correct option[y/n]: "))

#Gets the current path
current_directory = os.getcwd()

# make log dir 
log_directory_name = r"hdmi_log/"
log_gen.mkdir(log_directory_name) 

# make log file
log_file_path = log_directory_name+"hdmi_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
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

# check the hdmi and sound card, then write information 
log_file.write("Aplay informations:\n")
sp_aplay = subprocess.Popen("aplay -l", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
aplay_console_lines = sp_aplay.stdout.readlines()
for i in aplay_console_lines:
    print(i.strip().decode("utf-8"))
    log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'
    
log_file.write("hdmi informations:\n")
sp_hdmi = subprocess.Popen("modeprint starfive", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
hdmi_console_lines = sp_hdmi.stdout.readlines()
for i in hdmi_console_lines:
    print(i.strip().decode("utf-8"))
    log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

# # play the audio information and write information
# log_file.write("hdmi test informations:\n")
# sp_hdmi_test = subprocess.Popen("modetest -M starfive -a -s 116@31:1920x1080 -P 39@31:1920x1080@YUYV -F tiles", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
# hdmi_test_console_lines = sp_hdmi_test.stdout.readlines()
# for i in hdmi_test_console_lines:
#     print(i.strip().decode("utf-8"))
#     log_file.write(str(i.strip().decode("utf-8")) + "\n") #remove'\n'and'b'

# os.system("modetest -M starfive -a -s 116@31:1920x1080 -P 39@31:1920x1080@YUYV -F tiles")
gst_command = "gst-launch-1.0 -v filesrc location=720p_h264_aac.mp4 ! qtdemux name=demux demux.audio_0 ! queue ! aacparse ! avdec_aac ! audioconvert ! alsasink device=hw:0,1 demux.video_0 ! queue ! h264parse ! omxh264dec ! videoscale ! video/x-raw,width=1280,height=720 ! kmssink driver-name=starfive force-modesetting=1"
os.system(gst_command)

test_result = input("Whether the video playback is clear and continuous, the audio playback is clear, continuous, and free of noise[y/n]: ")

while True:
    if test_result == "y":
        test_result = "hdmi test successful!"
        print(test_result+"\n")
        log_file.write(test_result)
        break
    elif test_result == "n":
        test_result = "hdmi test fail!\n"
        note_information = input("Please describe the phenomenon that occurred during the test: ")
        print(test_result+"\n")
        log_file.write("Note informations: " + test_result)
        log_file.write(note_information)
        break
    else:
        test_result = input("Please enter the correct options[y/n]: ")
        continue

# 显示结束时间
end_time = time.localtime(time.time())
print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  hdmi test finish  **********", sep="")

#写入结束时间
log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
log_file.close()

