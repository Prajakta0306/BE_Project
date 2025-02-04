import RPi.GPIO as GPIO
import dht11
import time

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=20)
#Thinkspeak
import sys
import urlopen
import urllib

from time import sleep
# Enter Your API key here
User1API = 'NWQRAVIZY6YYJWM6' 

# URL where we will send the data, Don't change it
baseURL1 = 'https://api.thingspeak.com/update?api_key=%s' % User1API

print("***********DHT 11 sensor activated ***********")
while True:
    result = instance.read()
    if result.is_valid():
        a = result.temperature
        print("Enviorment Tempreture:"+str(a))
        
        b = result.humidity
        print("Enviorment Humidity:"+str(b))
        print("-------------------------------")
        conn = baseURL1 + '&field1=%s&field2=%s' % (a , b)
        request = urllib.request.Request(conn)
        responce = urllib.request.urlopen(request)
        responce.close()
    
            
    
   
        

                                                           

 
 

