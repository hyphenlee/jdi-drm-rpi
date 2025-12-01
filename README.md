# ColorBerry

This repo is for jdi screen driver and configure file of ColorBerry, which is available on [discord](https://discord.gg/2uGPpVmCCE) and [Elecrow](https://www.elecrow.com/colorberry.html)

# jdi screen driver

support debian 11 32-bit and debian 12 64-bit with raspberry pi, and debian 12 64-bit with orange pi zero 2w

# Raspberry PI

## Install

### binary

* remove old jdi-drm

  ```shell
  sudo vi /boot/config.txt   
  # /boot/firmware/config.txt for debian 12
  sudo vi /etc/modules 
  sudo rm -f /boot/overlays/jdi-drm.dtbo 
  ```
* remove old sharp-drm in apt if exist, and other packages depend on it.
* unzip file to /var/tmp/jdi-drm-rpi
* cd to /var/tmp/jdi-drm-rpi
* run `sudo make install`
* reboot

### from source

* orangepi

```shell
sudo dpkg -i /opt/linux-headers-next-sun50iw9_1.0.0_arm64.deb
sudo orangepi-add-overlay sharp-drm.dts
make all
sudo cp sharp-drm.ko /lib/modules/6.1.31-sun50iw9/
sudo depmod -a
echo "sharp-drm" | sudo tee -a /etc/modules
```

* raspberry pi
  ```shell
  sudo apt-get install raspberrypi-kernel-headers
  make
  sudo make install
  ```



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

unzip `jdi-drm-orangepi-debian12-64.zip` file in any location and cd into it.

## install

```bash
sudo orangepi-add-overlay sharp-drm.dts
sudo cp sharp-drm.ko /lib/modules/6.1.31-sun50iw9/ # when upgrade, only need copy this file and reboot
sudo depmod -a
sudo echo "sharp-drm" >> /etc/modules 
# make sure only one sharp-drm in /etc/modules
```

## backlight

build [wiringOP-Python](https://github.com/orangepi-xunlong/wiringOP-Python/tree/next) with "next" branch, do the same as raspberry pi with `orangepi-back.py`

## .zshrc

```bash
if [ -z "$SSH_CONNECTION" ]; then
        if [[ "$(tty)" =~ /dev/tty ]] && type fbterm > /dev/null 2>&1; then
               fbterm
        elif [ -z "$TMUX" ] && type tmux >/dev/null 2>&1; then
                fcitx 2>/dev/null &
                tmux new -As "$(basename $(tty))"
        fi
fi

export PROMPT="%c$ "

alias d0="echo 0 | sudo tee /sys/module/sharp_drm/parameters/dither"
alias d3="echo 3 | sudo tee /sys/module/sharp_drm/parameters/dither"
alias d4="echo 4 | sudo tee /sys/module/sharp_drm/parameters/dither"
alias b="echo 1 | sudo tee /sys/module/sharp_drm/parameters/backlit"
alias bn="echo 0 | sudo tee /sys/module/sharp_drm/parameters/backlit"
alias key='echo "keys" | sudo tee /sys/module/beepy_kbd/parameters/touch_as > /dev/null'
alias mouse='echo "mouse" | sudo tee /sys/module/beepy_kbd/parameters/touch_as > /dev/null'
export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=14'
```

## .tmux.conf

```bash
# Status bar
set -g status-position top
set -g status-left ""
set -g status-right "#{ip} #{wifi_ssid} #{wifi_icon}|[#(cat /sys/firmware/beepy/battery_percent)]%H:%M"
set -g status-interval 10
set -g window-status-separator ' | '
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'gmoe/tmux-wifi'
set -g @plugin 'tmux-plugins/tmux-sensible'
run-shell ~/.tmux/plugins/tmux-plugin-ip/ip.tmux
run '~/.tmux/plugins/tpm/tpm'

set -g @tmux_wifi_icon_5 "☰"
set -g @tmux_wifi_icon_4 "☱"
set -g @tmux_wifi_icon_3 "⚌"
set -g @tmux_wifi_icon_2 "⚍"
set -g @tmux_wifi_icon_1 "⚊"
set -g @tmux_wifi_icon_off ""
```

## /etc/rc.local

```bash
echo 0 | sudo tee /sys/module/sharp_drm/parameters/dither
echo 0 | sudo tee /sys/firmware/beepy/keyboard_backlight > /dev/null
/usr/local/bin/gpio export 226 in
/usr/local/bin/gpio edge 226 rising
echo "key" | sudo tee /sys/module/beepy_kbd/parameters/touch_as > /dev/null
echo "always" | sudo tee /sys/module/beepy_kbd/parameters/touch_act > /dev/null
```

# xfce

```bash
sudo apt install task-xfce-desktop
sudo apt-get install xserver-xorg-legacy
sudo usermod -a orangepi -G tty
```

## /etc/X11/Xwrapper.config

```
	allowed_users=anybody
	needs_root_rights=yes
```

## /etc/X11/xorg.conf

```


Section "Device"
    Identifier "FBDEV"
    Driver "fbdev"
    Option "fbdev" "/dev/fb0"
#    Option "ShadowFB" "false"
EndSection

Section "ServerFlags"
    Option "BlankTime" "0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime" "0"
EndSection
```

# keyboard input under gui

copy file of gui-keymap/ to system file:

```
/usr/share/X11/xkb/symbols/us
/usr/share/X11/xkb/keycodes/evdev
```

map sym z,x,c...m to F1...F7,

shift - $ = F8

sym - $ = F9

sym - h = F10

sym - j = F11

sym - l = F12

sym - f = &

# [mgba](mgba.md) for playing gba game on ColorBerry
