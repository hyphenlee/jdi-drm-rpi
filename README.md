# jdi-drm

support debian 11 32-bit and debian 12 64-bit with raspberry pi, and debian 12 64-bit with orange pi zero 2w

## Install

* unzip file to /var/tmp/jdi-drm-rpi
* cd to /var/tmp/jdi-drm-rpi
* run `sudo make install`
* reboot

## Control backlight by side button

* put back.py in place like /home/username/sbin/back.py
* `chmod +x back.py`
* `sudo crontab -e`
* append `@reboot   sleep 5;/path/to/back.py`
* if it doesn't work in debian 12 64-bit, reinstall `python3-rpi.gpio`

### Set dithering level

```shell
echo <level> | sudo tee /sys/module/sharp_drm/parameters/dither > /dev/null
<level> from 0 to 4, 0 for close dithering, 4 for max
```

## .zshrc

```shell
if [ -z "$SSH_CONNECTION" ]; then
        if [[ "$(tty)" =~ /dev/tty ]] && type fbterm > /dev/null 2>&1; then
                fbterm
        # otherwise, start/attach to tmux
        elif [ -z "$TMUX" ] && type tmux >/dev/null 2>&1; then
                fcitx 2>/dev/null &
                tmux new -As "$(basename $(tty))"
        fi
fi
export PROMPT="%c$ "
export PATH=$PATH:~/sbin
export SDL_VIDEODRIVER="fbcon"
export SDL_FBDEV="/dev/fb1"
alias d0="echo 0 | sudo tee /sys/module/jdi_drm/parameters/dither"
alias d3="echo 3 | sudo tee /sys/module/jdi_drm/parameters/dither"
alias d4="echo 4 | sudo tee /sys/module/jdi_drm/parameters/dither"
alias b="echo 1 | sudo tee /sys/module/jdi_drm/parameters/backlit"
alias bn="echo 0 | sudo tee /sys/module/jdi_drm/parameters/backlit"
alias key='echo "keys" | sudo tee /sys/module/beepy_kbd/parameters/touch_as > /dev/null'
alias mouse='echo "mouse" | sudo tee /sys/module/beepy_kbd/parameters/touch_as > /dev/null'
```


# Orangepi zero 2W

Based on `Orangepizero2w_1.0.2_debian_bookworm_server_linux6.1.31.7z`

unzip file in any location and cd into it.

## install

```bash
sudo orangepi-add-overlay sharp-drm.dts
sudo cp sharp-drm.ko /lib/modules/6.1.31-sun50iw9/ # when upgrade, only need copy this file and reboot
sudo depmod -a
sudo echo "sharp-drm" >> /etc/modules 
# make sure only one sharp-drm in /etc/modules
```

## backlight

build [wiringOP-Python](https://github.com/orangepi-xunlong/wiringOP-Python/tree/next) with next branch, do the same as raspberry pi with `orangepi-back.py`
