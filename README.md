# jdi-drm-rpi

support debian 11 32-bit and debian 12 64-bit

## Install

* unzip file to /var/tmp/jdi-drm-rpi
* cd to /var/tmp/jdi-drm-rpi
* run `sudo make install`
* reboot

## Control backlight by side button

* put back.py in place like /home/username/sbin/back.py
* `chmod +x back.py`
* `sudo crontab -e`
* append `@reboot   /path/to/back.py`
* if it doesn't work in debian 12 64-bit, reinstall `python3-rpi.gpio`

### Set dithering level

```shell
echo <level> | sudo tee /sys/module/sharp_drm/parameters/dither > /dev/null
<level> from 0 to 4, 0 for close dithering, 4 for max
```
