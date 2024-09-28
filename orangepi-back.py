#!/bin/python3
import wiringpi
import os
import time
PIN = 5
backlit_on=False
init_label=False
last_time=time.time()
def gpio_callback():
    global init_label
    global last_time
    if time.time()-last_time<0.2:
        return
    last_time=time.time()
    if not init_label:
        return
    global backlit_on
    if backlit_on:
        backlit_on=False
        os.system("echo 0 | sudo tee /sys/module/sharp_drm/parameters/backlit > /dev/null")
        os.system("echo 0 | sudo tee /sys/firmware/beepy/keyboard_backlight > /dev/null")
    else:
        backlit_on=True
        os.system("echo 1 | sudo tee /sys/module/sharp_drm/parameters/backlit > /dev/null")
        os.system("echo 255 | sudo tee /sys/firmware/beepy/keyboard_backlight > /dev/null")

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(PIN, wiringpi.GPIO.PUD_UP)
wiringpi.wiringPiISR(PIN, wiringpi.GPIO.INT_EDGE_RISING, gpio_callback)
init_label=True

while True:
    wiringpi.delay(2000)