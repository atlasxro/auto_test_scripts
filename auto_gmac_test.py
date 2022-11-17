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

print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  开始gmac自动化测试  **********", sep="")

#获取gmac编号
gmac_num = int(input("请输入需要测试的gmac端口编号, 并确认已连接[0/1]: "))
while True:
    if gmac_num == 0 or gmac_num ==1:
        print("测试gmac_",gmac_num,sep="")
        break
    else:
        gmac_num = int(input("请输入正确的gmac端口编号[0/1]: "))
        continue

# def mkdir(path): #自定义日志文件夹创建函数
#     folder = os.path.exists(path)
#     if not folder:  #判断是否存在文件夹如果不存在则创建为文件夹
#         print("---  创建新的日志文件夹",  path, "  ---", sep="")
#         os.makedirs(path)  #makedirs 创建文件时如果路径不存在会创建这个路径
#         print("---  OK  ---")
#     else:
#         print("---  日志文件夹", path, "已存在!  ---", sep="")
        
# def mkfile(file):  #自定义创建文件函数
#     is_log_file = os.path.exists(file)
#     if not is_log_file:
#         print("---  创建新的日志文件：", file, "  ---", sep="")
#         logfile = open(file, 'w')
#         print("---  OK  ---")
#         logfile.close()
#     else:
#         print("---  日志文件：", file, "已存在!  ---", sep="")

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
log_file.write("***************开始测试时间: " + str(time.strftime('%y-%m-%d_%H:%M:%S',begin_time)) + "***************\n")

#写入系统信息
sys_info=open(r"/proc/version", "r")
sys_info_content = sys_info.read()
log_file.write("系统信息: " + sys_info_content)
sys_info.close()

#写入python版本
log_file.write("Python版本: " + platform.python_version() + "\n")

#写入iperf版本
iperf3_version = os.popen("iperf3 -v").readlines()
log_file.write("iperf3版本: " + iperf3_version[0])

#获取目标ip
server_ip=input("请输入server_ip: ")

#定义获取本机ip函数
def get_host_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

#获取本机ip
host_ip = get_host_ip()

#----------ping server并判断是否成功----------
def host_state(serverip):
    return True if os.system("ping -c 1 " + server_ip) is 0 else False

# host_state  = True if os.system("ping -c 1 " + server_ip) is 0 else False

while True:
    if host_state(server_ip):
        ping_result="本机:" + str(host_ip) + " ping " + "服务端:" + server_ip + "成功"
        print(ping_result)
        log_file.write(ping_result + "\n")
        break
    else:
        ping_result="本机:" + str(host_ip) + " ping " + "服务端:" + server_ip + "失败"
        print(ping_result)
        # log_file.write(ping_result + "\n")
        server_ip=input("请重新输入server_ip: ")
        continue

#----------选择传输模式为TCP/UDP----------
trans_mode = input("请选择传输模式[tcp/udp]: ")
while True:
    if trans_mode == "tcp":
        trans_mode_info = "传输模式为: " + trans_mode
        print(trans_mode_info)
        log_file.write(trans_mode_info + "; ")
        trans_mode = ""
        break
    elif trans_mode == "udp":
        trans_mode_info = "传输模式为: " + trans_mode
        print(trans_mode_info)
        log_file.write(trans_mode_info + "; ")
        trans_mode = "-u"
        break
    else:
        trans_mode = input("请选择正确的传输模式[tcp/udp]: ")
        continue

#----------选择传输方向正向/反向/双向----------
# trans_dires =[]
# trans_dire = input("请选择传输方向(正向/反向/双向[p/r/d)]): ")
# while True:
#     if trans_dire == "p":
#         trans_dire_info = "传输方向为: 正向"
#         print(trans_dire_info)
#         log_file.write(trans_dire_info + "; ")
#         trans_dires = ""
#         break
#     elif trans_dire == "r":
#         trans_dire_info = "传输方向为: 反向(-R)"
#         print(trans_dire_info)
#         log_file.write(trans_dire_info + "; ")
#         trans_dires = "-R"
#         break
#     elif trans_dire == "d":
#         trans_dire_info = "传输方向为: 双向(-d)"
#         print(trans_dire_info)
#         log_file.write(trans_dire_info + "; ")
#         trans_dires = "-d"
#         break
#     else:
#         trans_dire = input("请选择正确的传输方向(正向/反向/双向[p/r/d]): ")
#         continue
trans_dires = []
trans_dire = input("请选择传输方向(正向/反向/双向[p/r/d])): ")
while True:
    if len(trans_dires) == 0:
        if trans_dire == "p" or trans_dire == "r" or trans_dire == "d":
            trans_dires.append(trans_dire)
            continue
        else:
            trans_dire = input("请输入正确的传输方向(正向/反向/双向[p/r/d])): ")
            continue
    elif len(trans_dires) > 0 and len(trans_dires) < 3:
        trans_dire = input("是否还需测试其余传输方向(正向/反向/双向/退出[p/r/d/q])): ")
        if trans_dire == "q":
            break
        else:
            while True:
                if trans_dire == "p" or trans_dire == "r" or trans_dire == "d":
                    if trans_dire in trans_dires:
                        trans_dire = input("此传输方向已选择, 请再选一个[p/r/d]: ")
                        continue
                    else:
                        trans_dires.append(trans_dire)
                        break
                else:
                    trans_dire = input("请输入正确的传输方向(正向/反向/双向[p/r/d])): ")
                    continue
    else:
        print("已全部选择！")
        break

#再次整理并打印trans_dire信息
trans_dires_info = "测试" + str(len(trans_dires)) +"种传输方向: " + str(trans_dires)
print(trans_dires_info)
log_file.write(str(trans_dires) + "; ")
trans_dire_all = []
for i in trans_dires:
    if i == "p":
        trans_dire_all.append(" ")
    elif i == "r":
        trans_dire_all.append(" -R")
    else:
        trans_dire_all.append(" -d")
        
#----------选择每次传输的持续时间----------
trans_time = input("请输入传输持续时间(s): ")
while True:
    if trans_time.endswith("s"):
        trans_time_temp = trans_time[0:-1]
        if trans_time_temp.isnumeric():
            trans_time_info = "传输持续时间为: " + trans_time
            print(trans_time_info)
            log_file.write(trans_time_info + "; ")
            trans_time = "-t " + trans_time
            # print(trans_time)
            break
        else:
            trans_time = input("请检查格式是否正确并重新输入传输持续时间(s): ")
            continue
    else:
        trans_time = input("请检查格式是否正确并重新输入传输持续时间(s): ")
        continue

#----------输入带宽----------
# bandwidth = input("请输入约定带宽[M/G]: ")
# while True:
#     if bandwidth.endswith("M") or bandwidth.endswith("G"):
#         bandwidth_temp = bandwidth[0:-1]
#         if bandwidth_temp.isnumeric():
#             bandwidth_info = "约定带宽为: " + bandwidth
#             print(bandwidth_info)
#             log_file.write(bandwidth_info + "; ")
#             bandwidth = "-b " + bandwidth
#             break
#         else:
#             bandwidth = input("输入格式有误，清重新输入约定带宽[M/G]: ")
#             continue
#     else:
#         bandwidth = input("输入格式有误，请重新输入约定带宽[M/G]: ")
#         continue
bandwidths = []
bandwidth = input("请输入bandwidth[M/G/默认(0)]: ")
while True:
    if len(bandwidths) == 0:
        if bandwidth.isnumeric() and int(bandwidth) == 0:
            # bandwidth_info = "采用默认bandwidth传输"
            # print(bandwidth_info)
            bandwidth = ""
            break
        else:
            if bandwidth.endswith("M") or bandwidth.endswith("G"):
                bandwidth_tem = bandwidth[0:-1]
                if bandwidth_tem.isnumeric():
                    bandwidths.append(bandwidth)
                    continue
                else:
                    bandwidth = input("请按正确的格式输入bandwidth[M/G]: ")
                    continue
            else:
                bandwidth = input("请按正确的格式输入bandwidth[M/G]: ")
                continue
    else:
        bandwidth = input("是否还需其余bandwidth[M/G/q(退出)]: ")
        if bandwidth == "q":
            break
        else:
            while True:
                if bandwidth.endswith("M") or bandwidth.endswith("G"):
                    bandwidth_tem = bandwidth[0:-1]
                    if bandwidth_tem.isnumeric():
                        if bandwidth in bandwidths:
                            bandwidth = input("此bandwidth已存在, 请再选一个[M/G]: ")
                            continue
                        else:
                            bandwidths.append(bandwidth)
                            break
                    else:
                        bandwidth = input("请按正确的格式输入bandwidth[M/G]: ")
                        continue
                else:
                    bandwidth = input("请按正确的格式输入bandwidth[M/G]: ")
                    continue

bandwidth_M = []
bandwidth_G = []
bandwidth_sizes = []
for M in bandwidths:
    if M.endswith("M"):
        M = M[0:-1]
        bandwidth_M.append(int(M))

bandwidth_M.sort()
# print(bandwidth_M)

for M in bandwidth_M:
    M = str(M) + "M"
    bandwidth_sizes.append(M)

for G in bandwidths:
    if G.endswith("G"):
        G = G[0:-1]
        bandwidth_G.append(int(G))
        
bandwidth_G.sort()
# print(bandwidth_G)

for G in bandwidth_G:
    G = str(G) + "G"
    bandwidth_sizes.append(G)

#再次整理并打印bandwidth信息
bandwidth_all = []#定义一个用到命令中的bandwidth变量数组
if len(bandwidth_sizes) == 0:
    bandwidth_info = "采用默认bandwidth参数进行测试"
    print(bandwidth_info)
    log_file.write(bandwidth_info + "; ")
    bandwidth_all = ""
else: 
    bandwidth_info = "采用" + str(len(bandwidth_sizes)) +"种bandwidth参数进行测试: " + str(bandwidth_sizes)
    print(bandwidth_info)
    log_file.write(bandwidth_info + "; ")
    for i in bandwidth_sizes:
        bandwidth_all.append("-b " + str(i))
   
#----------选择是否需要并行----------
# is_parallel = input("输入需要的并行传输数[0(不需要)]: ")
# while True:
#     if is_parallel.isnumeric():
#         if int(is_parallel) > 0:
#             is_parallel_info = "并行传输: " + is_parallel
#             print(is_parallel_info)
#             log_file.write(is_parallel_info + "; ")
#             is_parallel = "-P " + is_parallel
#             break
#         elif int(is_parallel) == 0:
#             is_parallel_info = "无并行传输"
#             print(is_parallel_info)
#             log_file.write(is_parallel_info + "; ")
#             is_parallel = ""
#             break
#         else:
#             is_parallel = input("输入格式有误，请重新输入: ")
#             continue
#     else:
#         is_parallel = input("输入格式有误，请重新输入: ")
#         continue   

parallels = []
parallel = input("输入需要的并行传输数[0(不需要)]: ")
while True:
    if len(parallels) == 0:
        if parallel.isnumeric() and int(parallel) == 0:
            # parallel_info = "不采用parallel传输"
            # print(parallel_info)
            parallel = ""
            break
        else:
            if parallel.isnumeric() and int(parallel) > 0:
                parallels.append(parallel)

            else:
                parallel = input("请按正确的格式输入parallel: ")
                continue
    else:
        parallel = input("是否还需其余parallel[q(退出)]: ")
        if parallel == "q":
            break
        else:
            while True:
                if parallel.isnumeric() and int(parallel) > 0:
                    if parallel in parallels:
                        parallel = input("此parallel已存在, 请再选一个: ")
                        continue
                    else:
                        parallels.append(parallel)
                        break
                else:
                    parallel = input("请按正确的格式输入parallel: ")
                    continue

# parallels = parallels.sort()

#再次整理并打印parallels信息
parallel_all = []#定义一个用到命令中的parallels变量数组
if len(parallels) == 0:
    parallel_info = "不采用parallel传输"
    print(parallel_info)
    log_file.write(parallel_info + "; ")
    parallel_all = ""
else: 
    parallel_info = "采用" + str(len(parallels)) +"种Buffer size传输: " + str(parallels)
    print(parallel_info)
    log_file.write(parallel_info + "; ")
    for i in parallels:
        parallel_all.append("-P " + str(i))

#----------获取需要测试的buffer size----------
buffers = []
buffer = input("请输入buffer size[b/k/默认(0)]: ")
while True:
    if len(buffers) == 0:
        if buffer.isnumeric() and int(buffer) == 0:
            # buffer_info = "采用默认Buffer size传输"
            # print(buffer_info)
            # log_file.write(buffer_info + "; ")
            # buffers.append("0")
            break
        else:
            if buffer.endswith("b") or buffer.endswith("k"):
                buffer_tem = buffer[0:-1]
                if buffer_tem.isnumeric():
                    buffers.append(buffer)
                    continue
                else:
                    buffer = input("请按正确的格式输入buffer size[b/k]: ")
                    continue
            else:
                buffer = input("请按正确的格式输入buffer size[b/k]: ")
                continue
    else:
        buffer = input("是否还需其余buffer size[b/k/q(退出)]: ")
        if buffer == "q":
            break
        else:
            while True:
                if buffer.endswith("b") or buffer.endswith("k"):
                    buffer_tem = buffer[0:-1]
                    if buffer_tem.isnumeric():
                        if buffer in buffers:
                            buffer = input("此buffer size已存在, 请再选一个[b/k]: ")
                            continue
                        else:
                            buffers.append(buffer)
                            break
                    else:
                        buffer = input("请按正确的格式输入buffer size[b/k]: ")
                        continue
                else:
                    buffer = input("请按正确的格式输入buffer size[b/k]: ")
                    continue

#buffer size排序
buffer_size_b = []
buffer_size_k = []
buffer_sizes = []
buffer_sizes_all = []#定义一个用到命令中的buffer size变量数组
if len(buffers) > 0:
    for b in buffers:
        if b.endswith("b"):
            b = b[0:-1]
            buffer_size_b.append(int(b))

    buffer_size_b.sort()
    # print(buffer_size_b)

    for b in buffer_size_b:
        b = str(b) + "b"
        buffer_sizes.append(b)

    for k in buffers:
        if k.endswith("k"):
            k = k[0:-1]
            buffer_size_k.append(int(k))
        
    buffer_size_k.sort()
    # print(buffer_size_k)

    #b->k整理好的 buffer_sizes
    for k in buffer_size_k:
        k = str(k) + "k"
        buffer_sizes.append(k)

    #再次整理并打印buffer信息
    if len(buffers) == 0:
        buffer_info = "采用默认Buffer size传输"
        print(buffer_info)
        log_file.write(buffer_info + "; ")
        buffer_sizes_all = ""
    else: 
        buffer_info = "采用" + str(len(buffer_sizes)) +"种Buffer size传输: " + str(buffer_sizes)
        print(buffer_info)
        log_file.write(buffer_info + "; ")
        for i in buffer_sizes:
            buffer_sizes_all.append("-l " + str(i))
        # print(buffer_sizes_all)
else:
    buffer_sizes_all.append(" ")


#运行iperf
for trans_direi in trans_dire_all:
# for trains_direi in trans_dires:
    if len(parallel_all) > 0:
        for is_parallel in parallel_all:
            if len(bandwidth_all) > 0:
                for bandwidth_i in bandwidth_all:
                    if len(buffer_sizes_all) > 0:
                        for buffer_size in buffer_sizes_all:
                            iperf3_command = "iperf3 -c"
                            iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + bandwidth_i + " " + buffer_size + " " + is_parallel
                            print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                            print("\n" + "\n"+ "----------" + iperf3_command + "----------", file=log_file)
                            # print(os.system(iperf3_command), file=log_file)
                            # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                            sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                            console_lines = sp.stdout.readlines()
                            for i in console_lines:
                                print(i.strip().decode("utf-8"))
                            console_lines_last = console_lines[-5:-2]
                            for i in console_lines_last:
                                log_file.write(str(i.strip().decode("utf-8")) + "\n") #去除输出的转义符'\n'以及开头的字节数组标志'b'
                    else:
                        iperf3_command = "iperf3 -c"
                        iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + bandwidth_i + " " + is_parallel
                        print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                        print("\n" + "\n" + "----------" + iperf3_command + "----------", file=log_file)
                        # print(os.system(iperf3_command), file=log_file)
                        # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                        sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                        console_lines = sp.stdout.readlines()
                        for i in console_lines:
                            print(i.strip().decode("utf-8"))
                        console_lines_last = console_lines[-5:-2]
                        for i in console_lines_last:
                            log_file.write(str(i.strip().decode("utf-8")) + "\n")
            else:
                if len(buffer_sizes_all) > 0:
                        for buffer_size in buffer_sizes_all:
                            iperf3_command = "iperf3 -c"
                            iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + buffer_size + " " + is_parallel
                            print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                            print("\n" + "\n"+ "----------" + iperf3_command + "----------", file=log_file)
                            # print(os.system(iperf3_command), file=log_file)
                            # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                            sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                            console_lines = sp.stdout.readlines()
                            for i in console_lines:
                                print(i.strip().decode("utf-8"))
                            console_lines_last = console_lines[-5:-2]
                            for i in console_lines_last:
                                log_file.write(str(i.strip().decode("utf-8")) + "\n") #去除输出的转义符'\n'以及开头的字节数组标志'b'
                else:
                    iperf3_command = "iperf3 -c"
                    iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + is_parallel
                    print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                    print("\n" + "\n" + "----------" + iperf3_command + "----------", file=log_file)
                    # print(os.system(iperf3_command), file=log_file)
                    # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                    sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                    console_lines = sp.stdout.readlines()
                    for i in console_lines:
                        print(i.strip().decode("utf-8"))
                    console_lines_last = console_lines[-5:-2]
                    for i in console_lines_last:
                        log_file.write(str(i.strip().decode("utf-8")) + "\n")
    else:
        if len(bandwidth_all) > 0:
            for bandwidth_i in bandwidth_all:
                if len(buffer_sizes_all) > 0:
                    for buffer_size in buffer_sizes_all:
                        iperf3_command = "iperf3 -c"
                        iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + bandwidth_i + " " + buffer_size
                        print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                        print("\n" + "\n"+ "----------" + iperf3_command + "----------", file=log_file)
                        # print(os.system(iperf3_command), file=log_file)
                        # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                        sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                        console_lines = sp.stdout.readlines()
                        for i in console_lines:
                            print(i.strip().decode("utf-8"))
                        console_lines_last = console_lines[-5:-2]
                        for i in console_lines_last:
                            log_file.write(str(i.strip().decode("utf-8")) + "\n") #去除输出的转义符'\n'以及开头的字节数组标志'b'
                else:
                    iperf3_command = "iperf3 -c"
                    iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + bandwidth_i
                    print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                    print("\n" + "\n" + "----------" + iperf3_command + "----------", file=log_file)
                    # print(os.system(iperf3_command), file=log_file)
                    # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                    sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                    console_lines = sp.stdout.readlines()
                    for i in console_lines:
                        print(i.strip().decode("utf-8"))
                    console_lines_last = console_lines[-5:-2]
                    for i in console_lines_last:
                        log_file.write(str(i.strip().decode("utf-8")) + "\n")
        else:
            if len(buffer_sizes_all) > 0:
                    for buffer_size in buffer_sizes_all:
                        iperf3_command = "iperf3 -c"
                        iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time + " " + buffer_size
                        print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                        print("\n" + "\n"+ "----------" + iperf3_command + "----------", file=log_file)
                        # print(os.system(iperf3_command), file=log_file)
                        # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                        sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                        console_lines = sp.stdout.readlines()
                        for i in console_lines:
                            print(i.strip().decode("utf-8"))
                        console_lines_last = console_lines[-5:-2]
                        for i in console_lines_last:
                            log_file.write(str(i.strip().decode("utf-8")) + "\n") #去除输出的转义符'\n'以及开头的字节数组标志'b'
            else:
                iperf3_command = "iperf3 -c"
                iperf3_command = iperf3_command + " " + server_ip + " " + trans_mode + " " + trans_direi + " " + trans_time
                print("\n" + "\n"+ "----------" + iperf3_command + "----------")
                print("\n" + "\n" + "----------" + iperf3_command + "----------", file=log_file)
                # print(os.system(iperf3_command), file=log_file)
                # print(subprocess.run(iperf3_command, shell=True, universal_newlines=True), file=log_file)
                sp = subprocess.Popen(iperf3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
                console_lines = sp.stdout.readlines()
                for i in console_lines:
                    print(i.strip().decode("utf-8"))
                console_lines_last = console_lines[-5:-2]
                for i in console_lines_last:
                    log_file.write(str(i.strip().decode("utf-8")) + "\n")


# 显示结束时间
end_time = time.localtime(time.time())
print("\n**********  " + time.strftime('%Y-%m-%d %H:%M:%S',end_time) + "  结束gmac自动化测试  **********", sep="")

#写入结束时间
log_file.write("\n" + "***************结束测试时间: " + str(time.strftime('%y-%m-%d_%H:%M:%S',end_time)) + "***************")
log_file.close()