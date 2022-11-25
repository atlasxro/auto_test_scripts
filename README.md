# auto_test_scripts

Python auto_test_scripts used in smoke test.  
Automatically generate logs containing information such as system, software version, and so on.

* main.py:  
The main program used to invoke each submodule.

* cfg.ini:  
Configuration file to decide whether to enable a submodule and modify parameters.

* log_gen.py:  
Log generation module.

* auto_gmac0/1_test:  
Test whether the network port is connected and the TCP transmission performance.

* auto_hdmi_test:  
Automatically detect screen support formats and play the 720_h264_aac.mp4, the result needs to be confirmed manually.

* auto_mipi_csi_test:  
Automatically detect the informations and support formats of screen and sensor and transfer the image to the screen via HDMI, the result needs to be confirmed manually.  
Notice: The ISP driver cannot be pulled up at the same time, and can only be tested when the display is green.

* auto_uvc_test:  
Automatically detect the informations and support formats of screen and sensor and transfer the image to the screen via HDMI, the result needs to be confirmed manually.  

* auto_mipi_dsi_test:  
Automatically detect the informations and support formats of screen and run the modetest to play the tiles image, the result needs to be confirmed manually.

* auto_pwmdac_test:  
Automatically detect the informations of sound card and play the audio.wav, the result needs to be confirmed manually.

* auto_sd_test.py:  
Automatically test the SD Card performance of read & write.

* auto_emmc_test.py:  
Automatically test the eMMC performance of read & write.  
Notice: Make sure that the eMMC has partitioned correctly and established the file system before testing.

* auto_pcie_ssd.py:  
Automatically test the PCIe_SSD performance of read & write.  
Notice: Make sure that the PCIe_SSD has partitioned correctly and established the file system before testing and determine that the supply voltage can drive PCIe_SSD.

* auto_usb_test.py:  
Automatically identify if a storage device plugged in the USB port and test the read and write performance.

* auto_gpio_test.py:  
Automatically test whether each GPIO port works normally, GPIO ports must be connected in pairs as described as the GPIO part in the cfg.ini before testing.

* Known issues:  
After running the main program, running it again may not start MIPI-DSI normally, the reason is unknown, it is recommended to restart the board before each complete testing.
