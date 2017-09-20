# raspberrypi
raspberry pi python scripts using polling

## Installation
sudo apt-get update

sudo apt-get -y install python-rpi.gpio


sudo nano /home/pi/shutdown.py

copy the script

sudo crontab -e
option 2 nano
@reboot sudo python /home/pi/shutdown.py

sudo python /home/pi/shutdown.py
