#!/bin/python3
import RPi.GPIO as GPIO
import signal
import sys
import subprocess
import os
from time import sleep, time
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
backlit_on=False
init_label=False
last_time=time()
def signal_handler(sig, frame):
    GPIO.cleanup()
    print("cleanup")
    sys.exit(0)
def button_pressed_callback(channel):
    global init_label
    global last_time
    global backlit_on
    if time()-last_time<0.2:
        return
    last_time=time()
    if not init_label:
        return
    if backlit_on:
        backlit_on=False
        os.system("echo 0 | sudo tee /sys/module/sharp_drm/parameters/backlit > /dev/null")
        os.system("echo 0 | sudo tee /sys/firmware/beepy/keyboard_backlight > /dev/null")
    else:
        backlit_on=True
        os.system("echo 1 | sudo tee /sys/module/sharp_drm/parameters/backlit > /dev/null")
        os.system("echo 255 | sudo tee /sys/firmware/beepy/keyboard_backlight > /dev/null")


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.RISING, 
            callback=button_pressed_callback, bouncetime=100)
    init_label=True
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
