#!/bin/bash

#Define GPIO pin 18 as PWM
gpio -g mode 18 pwm

#Always num = 0
num=0
while [ $num = 0 ]; do

# What's the CPU temp?
temp=$(cat /sys/class/thermal/thermal_zone0/temp)
temp=$(($temp/1000))

#Show the temperature
clear
printf "Temperatura: $tempºC\nVentilador activado."

# Variable temperature control
if

[ $temp -gt 40  ] && [ $temp -lt 69 ];
then
vartemp=$(echo $[temp * 13])
gpio -g pwm 18 $vartemp

# Maximum fan RPM
elif
[ $temp -ge 69 ];
then
gpio -g pwm 18 1024

# Switch off the fan
else
gpio -g pwm 18 0
clear
printf "Temperatura: $tempºC\nVentilador parado."
sleep 60
fi

#Pause 1 second
sleep 1

done
exit 0
