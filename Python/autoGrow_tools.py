import os
from datetime import time, datetime
from time import sleep
import RPi.GPIO as GPIO

# Check to see if current time is between range for light
def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end

# Switch lightState if current time is within specified 'on ' range
def controlLight(lightStart, lightEnd, lightPin):
    if in_between(datetime.now().time(), time(lightStart), time(lightEnd)):
        GPIO.output(lightPin, GPIO.LOW)
        lightState = 1
        return lightState
    else:
        lightState = 0
        GPIO.output(lightPin, GPIO.HIGH)
        return lightState

# Control the fans as a factor of whether or not the light is ON or OFF
def controlFan(lightState, fanDuration, fanPin):

    if lightState == 0:
        fanState = 0
        GPIO.output(fanPin, GPIO.HIGH)
        return fanState

    elif lightState == 1:
        if in_between(datetime.now().minute, 0, fanDuration):
            fanState = 1
            GPIO.output(fanPin, GPIO.LOW)
            return fanState
        else:
            fanState = 0
            GPIO.output(fanPin, GPIO.HIGH)
            return fanState

# Pulse  a pump with 5 second interval per specified time and frequency
def toggle_pump(pump_pin, time_on, pulses):

    i = 0
    while i < pulses:
        GPIO.output(pump_pin,GPIO.LOW)
        sleep(time_on)

        GPIO.output(pump_pin,GPIO.HIGH)
        sleep(5)

        i += 1

def system_status(light_state, fan_state, next_watering):

    print(datetime.now())
    message = ""

    if light_state == 1:
        message += "Light: On"
    else:
        message += "Light: Off"

    if fan_state == 1:
        message += "   Fan: On"
    else:
        message += "   Fan: Off"

    if next_watering == 0:
        message += "   No Waterings Yet"
    else:
        message += "   Next Watering: %s" % (next_watering)

    pi_temp = getCPUtemperature()
    message += "    Pi Temp: %s" % (pi_temp)

    print(message + '\n')

#Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

    







