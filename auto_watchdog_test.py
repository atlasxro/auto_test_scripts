#!/usr/bin/env python
# -*- coding: UTF-8 -*- 

import os
import time
import platform
import subprocess
import configparser

# import log_gen

get_timeleft_command = "cat /sys/class/watchdog/watchdog0/timeleft"
enable_wd_command = "echo 1 > /dev/watchdog0"
disable_wd_command = "echo 'V' > /dev/watchdog0"

count = 15
is_flag = 0

before_timelefe = os.popen(get_timeleft_command).readlines()[0].strip()

os.system(enable_wd_command)

while count >= 10:
    timelefe = os.popen(get_timeleft_command).readlines()[0].strip()
    if count == int(timelefe):
        count-=1
        print("test " + str(15-int(timelefe)) + " sec, timelefe=" + timelefe)
        time.sleep(1)
        continue
    else:
        print("test " + str(15-int(timelefe)) + " sec, fail!")
        is_flag = 1
        break

os.system(disable_wd_command)

after_timelefe = os.popen(get_timeleft_command).readlines()[0].strip()
if before_timelefe != after_timelefe:
    is_flag = 1

if is_flag == 0:
    print("Watchdog test Pass!")
else:
    print("Watchdog test Fail!")