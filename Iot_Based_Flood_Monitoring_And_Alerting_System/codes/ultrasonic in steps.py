import RPi.GPIO as GPIO
import time
#Thinkspeak
import sys
import urlopen
import urllib
GPIO.setwarnings(False) 
from time import sleep
# Enter Your API key here
User1API = 'NWQRAVIZY6YYJWM6' 

# URL where we will send the data, Don't change it
baseURL1 = 'https://api.thingspeak.com/update?api_key=%s' % User1API
    


# Define GPIO pins
TRIG_PIN = 27  # Trigger pin of ultrasonic sensor (BCM numbering)
ECHO_PIN = 17 # Echo pin of ultrasonic sensor (BCM numbering)
GREEN_LED_PIN = 26  # Green LED pin (BCM numbering)
YELLOW_LED_PIN = 19  # Yellow LED pin (BCM numbering)
RED_LED_PIN = 13  # Red LED pin (BCM numbering)
BUZZER_PIN = 21 # Buzzer pin (BCM numbering)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(GREEN_LED_PIN, GPIO.LOW)
GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
GPIO.output(RED_LED_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)

def measure_distance():
    # Send a pulse to trigger the ultrasonic sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start_time = time.time()

    # Measure the duration of pulse from the echo pin
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

    # Calculate distance in centimeters
    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def turn_on_green_led():
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def turn_on_yellow_led():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def turn_on_red_led():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.HIGH)

def turn_on_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def turn_off_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    while True:
        distance = measure_distance()
        print("Distance:", distance, "cm")
        conn = baseURL1 + '&field3=%s' % (distance)
        request = urllib.request.Request(conn)
        responce = urllib.request.urlopen(request)
        responce.close()

        if distance > 50:  # Normal level
            turn_on_green_led()
            turn_off_buzzer()
        elif 20 < distance <= 50:  # Medium level
            turn_on_yellow_led()
            turn_off_buzzer()
        else:  # High level (flood)
            turn_on_red_led()
            turn_on_buzzer()

        time.sleep(2)  # Adjust sleep time as per requirement

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
