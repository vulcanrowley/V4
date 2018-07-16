from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
import utime
# TMP36 analog temperature sensor
from machine import ADC

# ESP8266 ESP-12 modules have blue, active-low LED on GPIO2, replace
# with something else if needed.
led = Pin(2, Pin.OUT, value=1)

# Default MQTT server to connect to
SERVER = "192.168.1.117"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
subTOPIC = b"led"  # would be 'actuators' in more general version
pub_topic =b"sensors"
state = 0

''' Sensor reading  '''

# Define object
adc = ADC(0)

#function to read temperature
def  readTemp():
    temp =((adc.read()/10)*(9/5)) +32
    return temp

# define pin 13 as an input and activate an internal Pull-up resistor:
button = Pin(13, Pin.IN, Pin.PULL_UP)

# Function to read button state:
def readBut():
        return button.value()

# Function to read all data:
def collectData():
    temp = readTemp()
    butSts = readBut()
    return temp, butSts

''' Subscription setup '''

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(0)
        state = 1
    elif msg == b"off":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state


def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(subTOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, subTOPIC))

    try:
        while 1:
            c.check_msg()
            temp, butSts = collectData()
            payload = bytes("field1="+str(temp)+"&field5="+str(butSts),'utf-8') # or maybe json?
            c.publish(pub_topic, payload)
            utime.sleep(1)
    finally:
        c.disconnect()
		
main()

