#!/bin/bash

cd ~
sudo -H pip3 install Adafruit_BBIO
wget https://codeload.github.com/adafruit/Adafruit_Python_SSD1306/zip/master -O oled_screen.zip
unzip oled_screen.zip
cd Adafruit_Python_SSD1306*
sudo python3 setup.py install
