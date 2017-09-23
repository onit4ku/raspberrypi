# This script will wait for a button to be pressed and then shutdown
# the Raspberry Pi.

import time
from time import sleep
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)

# Pin 5 will be input and will have its pull-up resistor (to 3V3) activated
# so we only need to connect a push button with a current limiting resistor to ground
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# GPIO10 (on pin 23) will be our LED pin
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, GPIO.HIGH)
sleep(1)
GPIO.output(23, GPIO.LOW)

int_active = 0

# ISR: if our button is pressed, we will have a falling edge on pin 5
# this will trigger this interrupt:
def Int_shutdown(channel):

        # button is pressed
        # possibly shutdown our Raspberry Pi

        global int_active

        # only react when there is no other shutdown process running

        if (int_active == 0):

                int_active = 1
                pressed = 1

                shutdown = 0

                # turn LED on
                GPIO.output(23, GPIO.HIGH)

                # count how long the button is pressed

                counter = 0

                while ( pressed == 1 ):

                        if ( GPIO.input(5) == False ):

                                # button is still pressed

                                counter = counter + 1

                                # break if we count beyond 20 (long-press is a shutdown)
                                if (counter >= 20):

                                        pressed = 0

                                else:

                                        sleep(0.2)


                        else:
                                # button has been released

                                pressed = 0

                # button has been released, dim LED, count cycles and determine action

                GPIO.output(23, GPIO.LOW)


                # count how long the button was pressed

                if (counter < 2):

                        # short press, do nothing
                        pressed = 0
                        int_active = 0

                else:
                        # longer press


                        if (counter < 20):

                                # medium length press, initiate system reboot

                                print("rebooting..")

                                # run the reboot command as a background process
                                os.system("shutdown -r 0&")

                                # blink fast until the system stops
                                blink = 1
                                while (blink > 0):

                                        sleep(0.15)
                                        GPIO.output(23, GPIO.HIGH)
                                        sleep(0.15)
                                        GPIO.output(23, GPIO.LOW)

                        else:

                                # long press, initiate system shutdown

                                print("shutting down..")

                                # run the shutdown command as a background process
                                os.system("shutdown -h 0&")

                                # blink slow until system stops
                                blink = 1
                                while (blink > 0):

                                        sleep(1)
                                        GPIO.output(23, GPIO.HIGH)
                                        sleep(1)
                                        GPIO.output(23, GPIO.LOW)


# Now we are programming pin 5 as an interrupt input
# it will react on a falling edge and call our interrupt routine "Int_shutdown"
GPIO.add_event_detect(5, GPIO.FALLING,  callback = Int_shutdown, bouncetime = 1000)

# blink once every couple of seconds while waiting for button to be pressed
while 1:

        time.sleep(10)

        # only blink when the button isn't pressed
        if ( GPIO.input(5) == True ):

                # only blink when there's no shutdown in progress
                if (int_active == 0):

                        GPIO.output(23, GPIO.HIGH)
                        sleep(0.1)
                        GPIO.output(23, GPIO.LOW)
                        sleep(0.1)

# That's all folks!