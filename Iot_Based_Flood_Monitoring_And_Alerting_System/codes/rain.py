import RPi.GPIO as GPIO
import time
import requests


# Define GPIO pins
RAIN_SENSOR_PIN = 16  # GPIO pin where the rain sensor output is connected
buzzer = 21

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.setwarnings(False) 
print("Rain Sensor Ready.....")
print(" ")

#Thinkspeak
import sys
import urlopen
import urllib


    
from time import sleep
# Enter Your API key here
User1API = 'NWQRAVIZY6YYJWM6' 

# URL where we will send the data, Don't change it
baseURL1 = 'https://api.thingspeak.com/update?api_key=%s' % User1API
    



msg="Rain detected..So you have fine 500Rs."
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




try:
    while True:
        c = GPIO.input(RAIN_SENSOR_PIN)
        print(c)
        if GPIO.input(RAIN_SENSOR_PIN) == GPIO.LOW:
            print("It's raining!")
            sms_send()
        else:
            print("It's not raining.")
            conn = baseURL1 + '&field3=%s' % (c)
            request = urllib.request.Request(conn)
            responce = urllib.request.urlopen(request)
            responce.close()
        
        time.sleep(1)  # Check rain status every 1 second

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
