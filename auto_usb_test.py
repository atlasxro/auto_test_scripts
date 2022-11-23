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
cfg_section = "USB"

# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')
usbcnt = conf.getint(cfg_section, 'usbcnt')
usb1device = conf.get(cfg_section, 'usb1device')
usb2device = conf.get(cfg_section, 'usb2device')
usb3device = conf.get(cfg_section, 'usb3device')
usb4device = conf.get(cfg_section, 'usb4device')
blocksize = conf.get(cfg_section, 'blocksize')
blockcnt = conf.get(cfg_section, 'blockcnt')
expectspeed = conf.get(cfg_section, 'expectspeed')

if enable == "y":
    # show start time
    begin_time = time.localtime(time.time())

    print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start USB test  **********", sep="")

    # get current dir
    current_directory = os.getcwd()

    # make log dir
    log_directory_name = "usb_log"
    log_gen.mkdir(log_directory_name)

    # make log file
    log_file_path = str(log_directory_name)+r"/"+"usb" + "_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
    log_gen.mkfile(log_file_path)

    # open log file
    log_file = open(str(log_file_path), "w")

    # write start time
    log_file.write("***************Start test time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',begin_time)) + "***************\n")

    # write system info
    sys_info=open(r"/proc/version", "r")
    sys_info_content = sys_info.read()
    log_file.write("system information: " + sys_info_content)
    sys_info.close()

    # write python version
    log_file.write("Python version: " + platform.python_version() + "\n")

    cnt = 1
    passcnt = 0
    result_des = ""
    rinfo = []
    winfo = []
    
    while cnt <= usbcnt:
        print("Start USB " + str(cnt) + " test")
        if cnt == 1:
            usb_device = usb1device
        elif cnt == 2:
            usb_device = usb2device
        elif cnt == 3:
            usb_device = usb3device
        else:
            usb_device = usb4device
        
        # Determine whether the corresponding USB port is working
        str_wrong_msg = "port" + str(cnt) + ": Cannot enable. Maybe the USB cable is bad?"
        
        # define command 
        usb_wrong_test_command = "dmesg | grep -c " + "'" + str_wrong_msg + "'"
        log_file.write("Run test:\n" + usb_wrong_test_command)
        # usb_wrong_test_command = "exec " + usb_wrong_test_command + " 2>&1 | tee tempfile_wrong"
        sp_wrong = subprocess.Popen(usb_wrong_test_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        wrong_result = sp_wrong.stdout.readlines()[0].strip().decode("utf-8")
        
        # print(wrong_result)
        if int(wrong_result) > 0:
            str_wrong_msg = "wrong"
        else:
            str_wrong_msg = ""
        print(str_wrong_msg)
        
        # determine if the device exists
        usb_path = r"/dev/" + usb_device
        log_file.write("testing " + usb_device)
        is_exist_device = os.path.exists(usb_path)

        # run test
        if is_exist_device:
            # make a temp file to store the results temporary
            tempfile_r_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_r"
            tempfile_r = open(str(tempfile_r_path), 'w')
            tempfile_r.close()
            
            print("USB device " + usb_device + " exists!")
            
            # define read command 
            usb_r_test_command = "time dd if=" + usb_path + " of=/dev/null bs=" + blocksize + " count=" + blockcnt + " iflag=direct"
            print("Run test:\n" + usb_r_test_command)
            log_file.write("Run test:\n" + usb_r_test_command + "\n")
            usb_r_test_command = usb_r_test_command + " 2>&1 | tee tempfile_r"
            os.system(usb_r_test_command)
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
                rmsg = "USB device " + str(cnt) + ":" + usb_device + " READ: PASS  read speed: " + rspeed
                print(rmsg)
                log_file.write(rmsg + "\n")
                rinfo.append(rmsg)
            else:
                rmsg = "USB device " + str(cnt) + ":" + usb_device + " READ: FAIL  read speed slow: " + rspeed
                print(rmsg)
                log_file.write(rmsg + "\n")
                rinfo.append(rmsg)

            tempfile_w_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_w"
            tempfile_w = open(str(tempfile_w_path), 'w')
            tempfile_w.close()
                
            # define write command 
            usb_w_test_command = "time dd if=/dev/zero" + " of=" + usb_path + " bs=" + blocksize + " count=" + blockcnt
            print("Run test:\n" + usb_w_test_command)
            log_file.write("Run test:\n" + usb_w_test_command)
            usb_w_test_command = usb_w_test_command + " 2>&1 | tee tempfile_w"
            os.system(usb_w_test_command)
            w_result = open("tempfile_w", "r")
            w_results = w_result.readlines()
            for i in w_results:
                log_file.write(i.strip() + "\n")
            w_speed_info = w_results[2].strip()
            
            # get the read speed
            wspeed = w_speed_info.split(',')[-1].strip()
            wspeed_num = wspeed[0:-4]
            # print(wspeed)

            if wspeed != "" and float(wspeed_num) >= float(expectspeed):
                wmsg = "USB device " + str(cnt) + ":" + usb_device + " WRITE: PASS  write speed: " + wspeed + "\n"
                print(wmsg)
                log_file.write(wmsg + "\n")
                winfo.append(wmsg)
            else:
                wmsg = "USB device " + str(cnt) + ":" + usb_device + " WRITE: FAIL  write speed: " + wspeed + "\n"
                print(wmsg)
                log_file.write(wmsg + "\n")
                winfo.append(wmsg)
            
        else:
            print("No usb device " + str(cnt) + " exists, please check if the usb device is installed properly")
        
        cnt+=1
    
    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  USB test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()

else:
    print("USB not tested!")