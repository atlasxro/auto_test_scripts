#!/usr/bin/env python

import os
import time
import platform

import log_gen

# 显示开始时间
begin_time = time.localtime(time.time())

print("**********  " + time.strftime('%Y-%m-%d %H:%M:%S',begin_time) + "  start auto test  **********", sep="")

current_path = os.getcwd()

#创建日志文件
log_file_all_path = current_path + r"/" + "log_all" + ".txt"
log_gen.mkfile(log_file_all_path)

log_file_all = open("log_all.txt", "w")

#写入开始时间
log_file_all.write("***************Start test time: " + str(time.strftime('%y-%m-%d_%H:%M:%S',begin_time)) + "***************\n")

#写入系统信息
sys_info=open(r"/proc/version", "r")
sys_info_content = sys_info.read()
log_file_all.write("system information: " + sys_info_content)
sys_info.close()

#写入python版本
log_file_all.write("Python version: " + platform.python_version() + "\n")

# os.system(current_path + r"/auto_gmac_test.py")

# run hdmi_test
import auto_hdmi_test
if auto_hdmi_test.enable == "y":
    log_file_all.write("*****auto_hdmi_test*****\n")
    if auto_hdmi_test.test_result == "y":
        log_file_all.write(auto_hdmi_test.test_result_info)
    else:
        log_file_all.write(auto_hdmi_test.test_result_info)
        log_file_all.write(auto_hdmi_test.note_information)
else:
    log_file_all.write("#####HDMI not tested!#####\n")

# run dsi_test
import auto_mipi_dsi_test
if auto_mipi_dsi_test.enable == "y":
    log_file_all.write("*****auto_mipi_dsi_test*****\n")
    if auto_mipi_dsi_test.test_result == "y":
        log_file_all.write(auto_mipi_dsi_test.test_result_info)
    else:
        log_file_all.write(auto_mipi_dsi_test.test_result_info)
        log_file_all.write(auto_mipi_dsi_test.note_information)
else:
    log_file_all.write("#####MIPI_DSI not tested!#####\n")

# run csi_test
import auto_mipi_csi_test
if auto_mipi_csi_test.enable == "y":
    log_file_all.write("*****auto_mipi_csi_test*****\n")
    if auto_mipi_csi_test.test_result == "y":
        log_file_all.write(auto_mipi_csi_test.test_result_info)
    else:
        log_file_all.write(auto_mipi_csi_test.test_result_info)
        log_file_all.write(auto_mipi_csi_test.note_information)
else:
    log_file_all.write("#####MIPI_CSI not tested!#####\n")

# run pwmdac_test
import auto_pwmdac_test
if auto_pwmdac_test.enable == "y":
    log_file_all.write("*****auto_pwmdac_test*****\n")
    if auto_pwmdac_test.test_result == "y":
        log_file_all.write(auto_pwmdac_test.test_result_info)
    else:
        log_file_all.write(auto_pwmdac_test.test_result_info)
        log_file_all.write(auto_pwmdac_test.note_information)
else:
    log_file_all.write("#####PWMDAC not tested!#####\n")

# run sd_test
import auto_sd_test
if auto_sd_test.enable == "y":
    log_file_all.write("*****auto_sd_test*****\n")
    log_file_all.write(auto_sd_test.rmsg + "\n")
    log_file_all.write(auto_sd_test.wmsg + "\n")
else:
    log_file_all.write("#####SD not tested!#####\n")

# run pcie_ssd_test
import auto_pcie_ssd_test
if auto_pcie_ssd_test.enable == "y":
    log_file_all.write("*****auto_pcie_ssd_test*****\n")
    log_file_all.write(auto_pcie_ssd_test.rmsg + "\n")
    log_file_all.write(auto_pcie_ssd_test.wmsg + "\n")
else:
    log_file_all.write("#####PCIE_SSD not tested!#####\n")
    
# run emmc_test
import auto_emmc_test
if auto_emmc_test.enable == "y":
    log_file_all.write("*****auto_emmc_test*****\n")
    log_file_all.write(auto_emmc_test.rmsg + "\n")
    log_file_all.write(auto_emmc_test.wmsg + "\n")
else:
    log_file_all.write("#####eMMC not tested!#####\n")
    
# run usb_test
import auto_usb_test
if auto_usb_test.enable == "y":
    log_file_all.write("*****auto_usb_test*****\n")
    for i in auto_usb_test.is_exist_devices:
        log_file_all.write(i.strip() + "\n")
    log_file_all.write("\n")
    for i in auto_usb_test.rinfo:
        log_file_all.write(i.strip() + "\n")
    for i in auto_usb_test.winfo:
        log_file_all.write(i.strip() + "\n")
else:
    log_file_all.write("#####USB not tested!#####\n")
    
# run gpio_test
import auto_gpio_test
if auto_gpio_test.enable == "y":
    log_file_all.write("*****auto_gpio_test*****\n")
    log_file_all.write(auto_gpio_test.result_info + "\n")
    for i in auto_gpio_test.test_results:
        log_file_all.write(i + "\n")
else:
    log_file_all.write("#####gpio not tested!#####\n")

log_file_all.close