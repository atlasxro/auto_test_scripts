#!/usr/bin/env python
# -*- coding: UTF-8 -*- 

import os
import time
import platform
import configparser
import subprocess

import log_gen

# define cfg_name
cfg_name = "cfg.ini"

#获取gmac编号
gmac_num = 1

# indicates the location section of configuration in cfg_section
cfg_section = "GMAC" + str(gmac_num)

# instantation the class
conf = configparser.ConfigParser()

# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))

# get configuration
enable = conf.get(cfg_section, 'enable')


if enable == "y":
    # 显示开始时间
    begin_time = time.localtime(time.time())

    print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start gmac1 test  **********", sep="")


    #获取当前路径
    current_directory = os.getcwd()

    #创建对应gmac的日志目录 
    log_directory_name = "gmac_log"+r"/gmac_"+str(gmac_num)
    log_gen.mkdir(log_directory_name)  #调用函数

    #创建日志文件
    log_file_path = str(log_directory_name)+r"/"+"gmac"+str(gmac_num)+"_"+str(time.strftime('%y%m%d_%H%M%S',begin_time))+".txt"
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

    #写入iperf版本
    iperf3_version = os.popen("iperf3 -v").readlines()
    log_file.write("iperf3 version: " + iperf3_version[0])

    bandwidth = conf.get(cfg_section, 'baud')

    #获取目标ip
    server_ip = conf.get(cfg_section, 'vmip')

    #获取本机ip
    host_ip = conf.get(cfg_section, 'boardip')

    os.system("ifconfig eth" + str(gmac_num) + " " + host_ip + " netmask 255.255.255.0")
    os.system("ifconfig")

    #----------ping server并判断是否成功----------
    def host_state(serverip):
        return True if os.system("ping -c 1 " + server_ip) == 0 else False

    is_ping = host_state(server_ip)

    if is_ping:
        ping_result="gmac" + str(gmac_num) + " ip:" + host_ip + " ping " + "server:" + server_ip + " pass"
        print(ping_result)
        log_file.write(ping_result + "\n")
        
        expectbaudtcp = conf.get(cfg_section, 'expectbaudtcp')
        # print(expectbaudtcp)
        
        # timeout
        def terminate_func(thread_ter, stoptime):
            time.sleep(stoptime)
            thread_ter.terminate()
        
        # TX test
        tx_msg = "\nStart TX test"
        print(tx_msg)
        log_file.write(tx_msg)
        tempfile_tx_speed_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_tx_speed"
        tempfile_tx_speed = open(str(tempfile_tx_speed_path), 'w')
        tempfile_tx_speed.close()
        iperf3_tx_command = "iperf3 -c " + server_ip + " -b " + bandwidth + " -t 5 " + "-B " + host_ip
        # os.system(iperf3_tx_command + " 2>&1 | tee tempfile_tx_speed")
        sp_tx_command = subprocess.Popen("exec " + iperf3_tx_command + "  2>&1 | tee tempfile_tx_speed", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        terminate_func(sp_tx_command, 5 + 2)
        speed_tx_result = open("tempfile_tx_speed", "r")
        speed_tx_results = speed_tx_result.readlines()[-5:-2]
        for i in speed_tx_results:
            log_file.write(i.strip() + "\n")
        speed_tx_info = speed_tx_results[-1].strip()
        index_tx_speed = speed_tx_info.index("Mbits/sec")
        speed_tx_info = speed_tx_info[index_tx_speed-6:index_tx_speed].strip()
        # print(speed_tx_info)
        os.system("rm -f tempfile_tx_speed")
        if int(speed_tx_info) >= int(expectbaudtcp):
            tx_results = "ETH" + str(gmac_num) + " TCP TX SPEED PASS: " + speed_tx_info + " Mbits/sec"
            print(tx_results)
            log_file.write(tx_results)
        else:
            tx_results = "ETH" + str(gmac_num) + " TCP TX SPEED FAIL: " + speed_tx_info + " Mbits/sec"
            print(tx_results)
            log_file.write(tx_results)
        
        # RX test
        rx_msg = "\nStart RX test"
        print(rx_msg)
        log_file.write(rx_msg)
        tempfile_rx_speed_path = os.path.abspath(os.path.dirname(__file__)) + r"/tempfile_rx_speed"
        tempfile_rx_speed = open(str(tempfile_rx_speed_path), 'w')
        tempfile_rx_speed.close()
        iperf3_rx_command = "iperf3 -c " + server_ip + " -b " + bandwidth + " -t 5 " + "-R -B " + host_ip
        # os.system(iperf3_rx_command + "  2>&1 | tee tempfile_rx_speed")
        sp_rx_command = subprocess.Popen("exec " + iperf3_rx_command + "  2>&1 | tee tempfile_rx_speed", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        terminate_func(sp_rx_command, 5 + 2)
        speed_rx_result = open("tempfile_rx_speed", "r")
        speed_rx_results = speed_rx_result.readlines()[-5:-2]
        for i in speed_rx_results:
            log_file.write(i.strip() + "\n")
        speed_rx_info = speed_rx_results[-1].strip()
        index_rx_speed = speed_rx_info.index("Mbits/sec")
        speed_rx_info = speed_rx_info[index_rx_speed-6:index_rx_speed].strip()
        print(speed_rx_info)
        os.system("rm -f tempfile_rx_speed")
        if int(speed_rx_info) >= int(expectbaudtcp):
            rx_results = "ETH" + str(gmac_num) + " TCP RX SPEED PASS: " + speed_rx_info + " Mbits/sec"
            print(rx_results)
            log_file.write(rx_results)
        else:
            rx_results =  "ETH" + str(gmac_num) + " TCP RX SPEED FAIL: " + speed_rx_info + " Mbits/sec"
            print(rx_results)
            log_file.write(rx_results)
    else:
        ping_result="gmac" + str(gmac_num) + " ip:" + host_ip + " ping " + "server:" + server_ip + "fail, test fail"
        print(ping_result)
        log_file.write(ping_result + "\n")
else:
    print("GMAC" + str(gmac_num) + " not tested!")