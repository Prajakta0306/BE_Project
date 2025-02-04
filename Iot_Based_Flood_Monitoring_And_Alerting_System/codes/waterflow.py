import RPi.GPIO as GPIO
import time
import requests
# Define GPIO pins
FLOW_SENSOR_PIN = 6  # Use GPIO 14 (BCM) or pin 8 (BOARD)
BUZZER_PIN = 21       # Use GPIO 18 (BCM) or pin 12 (BOARD)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

#Thinkspeak
import sys
import urlopen
import urllib
from time import sleep
# Enter Your API key here
User1API = 'NWQRAVIZY6YYJWM6' 

# URL where we will send the data, Don't change it
baseURL1 = 'https://api.thingspeak.com/update?api_key=%s' % User1API
    




msg="Theft detected..So you have fine 500Rs."
def sms_send():
    url="https://www.fast2sms.com/dev/bulk"
    params={
  
        "authorization":"vTcAbIqUX3gjrDGOEBPhZxdLka2nf8Qy6etsMoYW47SzHmiVw9XwN2MVB74PhJye8ZEYsGOWv3fgcLaQ",
        "sender_id":"SMSINI",
        "message":msg,
        "language":"english",
        "route":"p",
        "numbers":"8530198249"
    }
    rs=requests.get(url,params=params)




def countPulse(channel):
    global pulses
    pulses += 1

def buzz_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzz_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# Configure event detection
GPIO.add_event_detect(FLOW_SENSOR_PIN, GPIO.FALLING, callback=countPulse, bouncetime=20)

# Main loop
pulses = 0
try:
    while True:
        time.sleep(1)
        flow_rate = pulses / 7.5  # Pulse frequency to flow rate conversion, adjust according to your sensor
        print("Flow rate: %.2f L/min" % flow_rate)
        conn = baseURL1 + '&field4=%s' % (flow_rate)
        request = urllib.request.Request(conn)
        responce = urllib.request.urlopen(request)
        responce.close()
        
        # Check if flow rate exceeds a certain threshold (example: 10 L/min)
        if flow_rate > 6:
            print("High water flow detected! Activating buzzer...")
            buzz_on()
            sms_send()
        else:
            buzz_off()

        pulses = 0  # Reset pulse count for the next interval

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
