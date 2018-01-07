# AutoGrow Project
# Description: Control lights, fans, and pumps, and record data from temp/humidity/soil moisture sensors in Poda.

# Import libraries
import sys
import schedule
import time
from datetime import datetime, time
from autoGrow_tools import *
import RPi.GPIO as GPIO

# Setup pins for components
fanPin = 25
lightPin = 7
pump_pin_1 = 23
#pump_pin_2 = 15
#atmoPin = 4
#soilMoisturePin1 = 5
#soilMoisturePin2 = 6

# Setup states for components
fanState = 0
lightState = 0
next_watering = 0

# Setup GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
    
# Establish GPIO pin orientation for all components
GPIO.setup(fanPin, GPIO.OUT) 
GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(pump_pin_1, GPIO.OUT)
#GPIO.setup(atmoPin, GPIO.IN)
#GPIO.setup(soilMoisturePin1, GPIO.IN)
#GPIO.setup(soilMoisturePin2, GPIO.IN)

# Start with light and fan OFF
GPIO.output(fanPin, GPIO.HIGH)
GPIO.output(lightPin, GPIO.HIGH)
GPIO.output(pump_pin_1, GPIO.HIGH)

# 'On' range for light (24-hour values)
lightStartHour = 18
lightEndHour = 6

# Length of fan duration in minutes
fanDuration = 15

# Schedule a repeating job for the watering
schedule.every(12).hours.do(toggle_pump,pump_pin_1, 0.25, 2)

# TODO
# Reformat "next watering" output
# write to log file and assess to see if fans contribute to pi cooling or heating
# install temp/humidity sensor, assess whether fans contribute to interior cooling

# Initiate infinite loop
while True:
    try:
        lightState = controlLight(lightStartHour, lightEndHour, lightPin)
        fanState = controlFan(lightState, fanDuration, fanPin)
        next_watering = schedule.next_run()
        system_status(lightState, fanState, next_watering)
        schedule.run_pending()
        sleep(30)
        
    # If anything fails, turn everything off (critical for water!)
    except:
        GPIO.output(fanPin, GPIO.HIGH)
        GPIO.output(lightPin, GPIO.HIGH)
        GPIO.output(pump_pin_1, GPIO.HIGH)
    

    

