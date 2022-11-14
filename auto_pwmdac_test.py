#!/usr/bin/env python

# -*- coding: UTF-8 -*- 

import os
import time
import sys
import platform
import socket
import subprocess

import log_gen

# 显示开始时间
begin_time = time.localtime(time.time())

print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  开始pwmdac自动化测试  **********", sep="")

os.system("ffmpeg -i audio.wav -f alsa -acodec pcm_s16le hw:0,0", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)