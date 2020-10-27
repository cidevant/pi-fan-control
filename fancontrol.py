#!/usr/bin/env python3

import os
import time
import RPi.GPIO as GPIO 

ON_THRESHOLD = 65  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 55  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 14  # Which GPIO pin you're using to control the fan.
  
def measure_CPU_temp():
        temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
        formatted_temp = temp.replace("\n", "")

        return int(float(temp) / 1000) 

# def measure_GPU_temp():
#         temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
#         formatted_temp = temp.replace("temp=","").replace("'C", "")
#         formatted_temp = formatted_temp.replace("\n", "")

#         return int(float(formatted_temp))

if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    is_running = False
    is_gpio_initialized = False

    while True:        
        if not is_gpio_initialized:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_PIN, GPIO.OUT)
            fan = GPIO.PWM(GPIO_PIN, 100)
            fan.start(0)
            fan.ChangeDutyCycle(100)
            time.sleep(5)
            fan.ChangeDutyCycle(0)
            fan.stop()
            GPIO.cleanup()    
            is_gpio_initialized = True
        
        temp_CPU = measure_CPU_temp()

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        if temp_CPU > ON_THRESHOLD and not is_running:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_PIN, GPIO.OUT)
            fan = GPIO.PWM(GPIO_PIN, 100)
            fan.start(0)
            fan.ChangeDutyCycle(100)
            is_running = True

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif is_running and temp_CPU < OFF_THRESHOLD:
            fan.ChangeDutyCycle(0)
            fan.stop()
            GPIO.cleanup()
            is_running = False

        time.sleep(SLEEP_INTERVAL)

    
