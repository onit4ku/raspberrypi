import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(04, GPIO.IN, pull_up_down = GPIO.PUD_UP)
while True:
    print GPIO.input(04)
    if(GPIO.input(04) == False):
        os.system("sudo shutdown -r now")
        break
    time.sleep(.1)
