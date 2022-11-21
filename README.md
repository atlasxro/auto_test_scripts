# auto_test_scripts

Python auto_test_scripts used in smoke test,.
Automatically generate logs containing information such as system, software version, and so on.

* auto_gmac_test:
Test whether the network port is connected and the transmission performance, whether the transfer mode, transfer direction, duration time, buffer size, parallel are selectable.
Known issues: problem with the format of the log generated when transferring in parallel.

* auto_hdmi_test:
Automatically detect screen support formats.

* auto_mipi_csi_test:
Automatically detect the informations and support formats of screen and sensor.
Known issues: The ISP driver cannot be pulled up at the same time, and can only be tested when the display is green.

* auto_mipi_dsi_test:
Automatically detect the informations and support formats of screen.

* auto_pwmdac_test:
Automatically detect the informations of sound card.
