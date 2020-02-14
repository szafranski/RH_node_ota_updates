# pins low/high as a function
# define number of pins
# flashed - only after success 

reset_1 = 12
reset_2 = 13
reset_3 = 16
reset_4 = 26

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
import os
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
GPIO.setup(reset_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(reset_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(reset_3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(reset_4, GPIO.OUT, initial=GPIO.LOW)

os.system("clear")
sleep(0.1)
print(" ")  
print(" ")
print(" ")
os.system("echo '     ###########################################################################################'")
os.system("echo '     ###                                                                                     ###'")
os.system("echo '     ###                                   RotorHazard                                       ###'")
os.system("echo '     ###                                                                                     ###'")
os.system("echo '     ###   You are about to update nodes firmware. Please do not interrupt this operation!   ###'")
os.system("echo '     ###                                                                                     ###'")
os.system("echo '     ###                                                                                     ###'")
os.system("echo '     ###########################################################################################'")
print(" ")
print(" ")
print(" ")

answer = None
while answer not in ("yes", "no"):
   answer = raw_input("           Do you want to proceed?    (yes) or (no):    ")
   if answer == "yes":
	sleep(0.1)
	os.system("sudo pkill server.py")
	os.system("sudo systemctl stop rotorhazard")
	sleep(0.1)

	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)

	sleep(0.1)
	os.system("sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
	os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:node.hex:i")


	os.system("echo")
	os.system("echo '     Node 1 - flashed'")
	os.system("echo")
	os.system("echo")
	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)


	sleep(0.1)
	os.system("sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
	os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:node.hex:i")


	os.system("echo")
	os.system("echo '     Node 2 - flashed'")
	os.system("echo")
	os.system("echo")
	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)
	sleep(0.1)
	os.system("sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
	os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:node.hex:i")


	os.system("echo")
	os.system("echo '     Node 3 - flashed'")
	os.system("echo")
	os.system("echo")
	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)
	sleep(0.1)

	os.system("sudo sed -i 's/reset .*/reset = 26;/g' /root/.avrduderc")
	os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:node.hex:i")

	os.system("sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")


	os.system("echo")
	os.system("echo '     Node 4 - flashed'")
	os.system("echo")
	os.system("echo")
	sleep(0.1)
	os.system("echo '     ########################################################################################'")
	os.system("echo '     ###                                                                                  ###'")
	os.system("echo '     ###  CONGRATULATIONS!              Flashing firmware to nodes - DONE                 ###'")
	os.system("echo '     ###                                                                                  ###'")
	os.system("echo '     ###  Please power off the timer, unplug voltage source for few seconds and reboot    ###'")
	os.system("echo '     ###                                                                                  ###'")
	os.system("echo '     ########################################################################################'")
	os.system("echo")
	os.system("echo")
	sleep(2)
   elif answer == "no":
	 print(" ")
	 print("OK - exiting")
	 print(" ")  
   else:
   	 print(" ")
	 print("Please enter yes or no.")
	 print(" ")  

