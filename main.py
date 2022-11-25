#!/usr/bin/env python

import os
import time
import platform
import configparser

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

## define cfg_name
cfg_name = "cfg.ini"
# instantation the class
conf = configparser.ConfigParser()
# import configuration file
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_name))


# run csi_test
if conf.get('CSI', 'enable') == "y":
    import auto_mipi_csi_test
    log_file_all.write("*****auto_mipi_csi_test*****\n")
    if auto_mipi_csi_test.test_result == "y":
        log_file_all.write(auto_mipi_csi_test.test_result_info + "\n")
    else:
        log_file_all.write(auto_mipi_csi_test.test_result_info)
        log_file_all.write(auto_mipi_csi_test.note_information + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####MIPI_CSI not tested!#####\n")

# run uvc_test
if conf.get('UVC', 'enable') == "y":
    import auto_uvc_test
    log_file_all.write("*****auto_uvc_test*****\n")
    if auto_uvc_test.test_result == "y":
        log_file_all.write(auto_uvc_test.test_result_info + "\n")
    else:
        log_file_all.write(auto_uvc_test.test_result_info)
        log_file_all.write(auto_uvc_test.note_information + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####UVC not tested!#####\n")

# run dsi_test
if conf.get('DSI', 'enable') == "y":
    import auto_mipi_dsi_test
    log_file_all.write("*****auto_mipi_dsi_test*****\n")
    if auto_mipi_dsi_test.test_result == "y":
        log_file_all.write(auto_mipi_dsi_test.test_result_info + "\n")
    else:
        log_file_all.write(auto_mipi_dsi_test.test_result_info)
        log_file_all.write(auto_mipi_dsi_test.note_information + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####MIPI_DSI not tested!#####\n")

# run pwmdac_test
if conf.get('PWMDAC', 'enable') == "y":
    import auto_pwmdac_test
    log_file_all.write("*****auto_pwmdac_test*****\n")
    if auto_pwmdac_test.test_result == "y":
        log_file_all.write(auto_pwmdac_test.test_result_info + "\n")
    else:
        log_file_all.write(auto_pwmdac_test.test_result_info)
        log_file_all.write(auto_pwmdac_test.note_information + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####PWMDAC not tested!#####\n")

# run hdmi_test
if conf.get('HDMI', 'enable') == "y":
    import auto_hdmi_test
    log_file_all.write("*****auto_hdmi_test*****\n")
    if auto_hdmi_test.test_result == "y":
        log_file_all.write(auto_hdmi_test.test_result_info + "\n")
    else:
        log_file_all.write(auto_hdmi_test.test_result_info)
        log_file_all.write(auto_hdmi_test.note_information + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####HDMI not tested!#####\n")

# run sd_test
if conf.get('SD', 'enable') == "y":
    import auto_sd_test
    log_file_all.write("*****auto_sd_test*****\n")
    log_file_all.write(auto_sd_test.rmsg + "\n")
    log_file_all.write(auto_sd_test.wmsg + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####SD not tested!#####\n")

# run pcie_ssd_test
if conf.get('PCIE_SSD', 'enable') == "y":
    import auto_pcie_ssd_test
    log_file_all.write("*****auto_pcie_ssd_test*****\n")
    log_file_all.write(auto_pcie_ssd_test.rmsg + "\n")
    log_file_all.write(auto_pcie_ssd_test.wmsg + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####PCIE_SSD not tested!#####\n")
    
# run emmc_test
if conf.get('EMMC', 'enable') == "y":
    import auto_emmc_test
    log_file_all.write("*****auto_emmc_test*****\n")
    log_file_all.write(auto_emmc_test.rmsg + "\n")
    log_file_all.write(auto_emmc_test.wmsg + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####eMMC not tested!#####\n")
    
# run usb_test
if conf.get('USB', 'enable') == "y":
    import auto_usb_test
    log_file_all.write("*****auto_usb_test*****\n")
    for i in auto_usb_test.is_exist_devices:
        log_file_all.write(i.strip() + "\n")
    log_file_all.write("\n")
    for i in auto_usb_test.rinfo:
        log_file_all.write(i.strip() + "\n")
    for i in auto_usb_test.winfo:
        log_file_all.write(i.strip() + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####USB not tested!#####\n")
    
# run gpio_test
if conf.get('GPIO', 'enable') == "y":
    import auto_gpio_test
    log_file_all.write("*****auto_gpio_test*****\n")
    log_file_all.write(auto_gpio_test.result_info + "\n")
    for i in auto_gpio_test.test_results:
        log_file_all.write(i + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####gpio not tested!#####\n")
    
# run gpio_test
if conf.get('TEMPERATURE', 'enable') == "y":
    import auto_temperature_test
    log_file_all.write("*****auto_temperature_test*****\n")
    log_file_all.write(auto_temperature_test.temp_msg + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####temperature not tested!#####\n")
    
# run gmac0_test
if conf.get('GMAC0', 'enable') == "y":
    import auto_gmac0_test
    log_file_all.write("*****auto_gmac0_test*****\n")
    log_file_all.write(auto_gmac0_test.tx_results + "\n")
    log_file_all.write(auto_gmac0_test.rx_results + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####gmac0 not tested!#####\n")
     
# run gmac1_test
if conf.get('GMAC1', 'enable') == "y":
    import auto_gmac1_test
    log_file_all.write("*****auto_gmac1_test*****\n")
    log_file_all.write(auto_gmac1_test.tx_results + "\n")
    log_file_all.write(auto_gmac1_test.rx_results + "\n")
    time.sleep(2)
else:
    log_file_all.write("#####gmac1 not tested!#####\n")

log_file_all.close