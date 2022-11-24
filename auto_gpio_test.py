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
cfg_section = "GPIO"

# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')

if enable == "y":
    # show start time
    begin_time = time.localtime(time.time())

    print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start GPIO test  **********", sep="")

    # get current dir
    current_directory = os.getcwd()

    # make log dir
    log_directory_name = "gpio_log"
    log_gen.mkdir(log_directory_name)

    # make log file
    log_file_path = str(log_directory_name)+r"/"+"gpio" + "_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
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
    
    failcnt = 0
    level = -1
    gpiochip = 0
    high = 1
    low = 0
    i = 0
    test_results = []
    
    while True:
        i+=1
        pinsnum = "pins" + str(i)
        # print(pinsnum)
        pinnum1_fail = 0
        pinnum2_fail = 0
        pins = conf.get(cfg_section, pinsnum)
        if pins == "-1":
            break
        pins = pins.split(",")
        pinnum1 = pins[0].strip()
        pinnum2 = pins[1].strip()
        # print(pinnum1)
        # print(pinnum2)

        # pinnum1 test
        print("gpio" + pinnum1 + " testing...\n")
        # pinnum1 set test
        # pinnum1 set high test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum1) + "=" + str(high)
        os.system(gpioset_command)
        # get pinnum2 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum2)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum1 + " set high test: " + "gpio" + str(pinnum1) + " set " + str(high) + " gpio" + str(pinnum2) + " get " + str(level))
        if level != high:
            print("gpio" + str(pinnum1) + " set " + str(high) + " fail")
            failcnt+=1
            pinnum1_fail+=1
        
        # pinnum1 set low test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum1) + "=" + str(low)
        os.system(gpioset_command)
        # get pinnum2 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum2)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum1 + " set low test: " + "gpio" + str(pinnum1) + " set " + str(low) + " gpio" + str(pinnum2) + " get " + str(level))
        if level != low:
            print("gpio" + str(pinnum1) + " set " + str(low) + " fail")
            failcnt+=1
            pinnum1_fail+=1
        
        # pinnum1 get test
        # pinnum1 get high test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum2) + "=" + str(high)
        os.system(gpioset_command)
        # get pinnum1 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum1)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum1 + " get high test: " + "gpio" + str(pinnum2) + " set " + str(high) + " gpio" + str(pinnum1) + " get " + str(level))
        if level != high:
            print("gpio" + str(pinnum1) + " get " + str(high) + " fail")
            failcnt+=1
            pinnum1_fail+=1
        
        # pinnum1 get low test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum2) + "=" + str(low)
        os.system(gpioset_command)
        # get pinnum1 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum1)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum1 + " get low test: " + "gpio" + str(pinnum2) + " set " + str(low) + " gpio" + str(pinnum1) + " get " + str(level))
        if level != low:
            print("gpio" + str(pinnum1) + " get " + str(low) + " fail")
            failcnt+=1
            pinnum1_fail+=1    

        if pinnum1_fail == 0:
            pinnum1_msg = "gpio" + str(pinnum1) + " test pass"
            print(pinnum1_msg)
            test_results.append(pinnum1_msg)
        else:
            pinnum1_msg = "FAIL: gpio" + str(pinnum1)
            print(pinnum1_msg)
            test_results.append(pinnum1_msg)
            
        # pinnum2 test
        print("gpio" + pinnum2 + " testing...\n")
        # pinnum2 set test
        # pinnum2 set high test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum2) + "=" + str(high)
        os.system(gpioset_command)
        # get pinnum1 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum1)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum2 + " set high test: " + "gpio" + str(pinnum2) + " set " + str(high) + " gpio" + str(pinnum1) + " get " + str(level))
        if level != high:
            print("gpio" + str(pinnum2) + " set " + str(high) + " fail")
            failcnt+=1
            pinnum2_fail+=1
        
        # pinnum2 set low test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum2) + "=" + str(low)
        os.system(gpioset_command)
        # get pinnum1 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum1)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum2 + " set low test: " + "gpio" + str(pinnum2) + " set " + str(low) + " gpio" + str(pinnum1) + " get " + str(level))
        if level != low:
            print("gpio" + str(pinnum2) + " set " + str(low) + " fail")
            failcnt+=1
            pinnum2_fail+=1
        
        # pinnum2 get test
        # pinnum2 get high test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum1) + "=" + str(high)
        os.system(gpioset_command)
        # get pinnum2 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum2)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum2 + " get high test: " + "gpio" + str(pinnum2) + " set " + str(high) + " gpio" + str(pinnum2) + " get " + str(level))
        if level != high:
            print("gpio" + str(pinnum2) + " get " + str(high) + " fail")
            failcnt+=1
            pinnum2_fail+=1
        
        # pinnum2 get low test
        gpioset_command = "gpioset " + "gpiochip" + str(gpiochip) + " " + str(pinnum1) + "=" + str(low)
        os.system(gpioset_command)
        # get pinnum2 level
        gpioget_command = "gpioget " + "gpiochip" + str(gpiochip) + " " + str(pinnum2)
        sp_gpioget_command = subprocess.Popen(gpioget_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        level = int(sp_gpioget_command.stdout.readlines()[0])
        print("gpio" + pinnum2 + " get low test: " + "gpio" + str(pinnum2) + " set " + str(low) + " gpio" + str(pinnum2) + " get " + str(level))
        if level != low:
            print("gpio" + str(pinnum2) + " get " + str(low) + " fail")
            failcnt+=1
            pinnum2_fail+=1    

        if pinnum2_fail == 0:
            pinnum2_msg = "gpio" + str(pinnum2) + " test pass"
            print(pinnum2_msg)
            test_results.append(pinnum2_msg)
        else:
            pinnum1_msg = "FAIL: gpio" + str(pinnum1)
            print(pinnum1_msg)
            test_results.append(pinnum1_msg)
    
    if failcnt == 0:
        result_info = "gpio test PASS!"
        print("\n" + result_info)
        log_file.write("\n" + result_info + "\n")
    else:
        result_info = "gpio test FAIL!"
        print("\n" + result_info)
        log_file.write("\n" + result_info + "\n")
        for i in test_results:
            print(i)
            log_file.write(i + "\n")

    # 显示结束时间
    end_time = time.localtime(time.time())
    print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  gpio test finish  **********", sep="")

    #写入结束时间
    log_file.write("\n" + "***************finish time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
    log_file.close()
else:
    print("GPIO not tested!")
        
