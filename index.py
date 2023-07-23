
import threading
import time
import socket
import RPi.GPIO as GPIO
from datetime import datetime

import paho.mqtt.client as paho
from paho import mqtt

import I2C_LCD_driver
import I2C_TSL2561_driver
from mfrc522 import SimpleMFRC522


# Configuration MQTT Broker
BROKER_ADDRESS = '6b7cae41985344b29aec77c29918cc12.s2.eu.hivemq.cloud'
BROKER_ADDRESS_TEMP = '098621d6f4574c228e8f49135e5aabfb.s2.eu.hivemq.cloud'
PORT = 8883
USER = 'raspi'
PASSWORD = 'Thang123'

TOPIC_REQUEST = "user/#"
TOPIC_RFID = "user/rfid/data"
TOPIC_TSL2561 = "user/tsl/data"

GPIO.setwarnings(False)

# LED bus
led_pin_rfid = 29
led_pin_tsl2561 = 31

# LCD 16x2
LCD_LINE_1 = 1
LCD_LINE_2 = 2

mylcd = I2C_LCD_driver.lcd()
rfid = SimpleMFRC522()

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

request_received = False

# Function to handle TSL2561
def read_tsl():
    while True:
        full_spectrum, visible, infrared = I2C_TSL2561_driver.read_tsl2561()    
        # Led = desk lamp, if visible < 500 -> led on
        tsl_data = f"Visible: {visible}, Infrared: {infrared}"
        if (visible < 500):
            GPIO.output(led_pin_tsl2561, GPIO.HIGH)
            light = True
        else:
            GPIO.output(led_pin_tsl2561, GPIO.LOW)
            light = False
        client.publish(TOPIC_TSL2561, tsl_data)
        
# Function to handle LCD
def display_realtime_info():
    while True:
        mylcd.lcd_display_string("Have2Grad", LCD_LINE_1)
        mylcd.lcd_display_string("%s"%time.strftime("%d/%m/%Y-%H:%M"), LCD_LINE_2)

# Function to handle RFID
def read_rfid():
    global request_received
    while True:
        try:
            if request_received:
                start_time = time.time()
                while time.time() - start_time < 10:
                    id, text = rfid.read_no_block()
                    if id is not None:
                        # Publish the data to HiveMQ
                        client.publish(TOPIC_RFID, payload = id, qos=0)
                        # Turn on the LED
                        GPIO.output(led_pin_rfid, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(led_pin_rfid, GPIO.LOW)
                        break
                    else:
                        time.sleep(0.1)
                # Continue to wait for the next request
                request_received = False
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise

# Function to handle MQTT connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe(TOPIC_REQUEST)  # Subscribe to the request topic
    client.subscribe("user/rfid") 
    client.subscribe(TOPIC_RFID)

# Function to handle MQTT message
def on_message(client, userdata, msg):
    global request_received
    if msg.topic == "user/rfid" and msg.payload.decode() == "check":
        request_received = True
        print(f"Received message on topic '{msg.topic}': check")

#Function to check Wi-Fi connectivity
def check_wifi():
    mylcd.lcd_display_string("Have2Grad", LCD_LINE_1)
    while True:
        try:
            # Try to connect to a known Wi-Fi access point
            socket.create_connection(("www.google.com", 80))
            mylcd.lcd_display_string("Wifi: connected", LCD_LINE_2)
            # Wi-Fi is connected, break the loop and proceed with the program
            time.sleep(2)
            break
        except (socket.error, OSError):
            mylcd.lcd_display_string("Wifi: waiting", LCD_LINE_2)
            # Wi-Fi is not connected, wait for a while and try again
            time.sleep(5)

# Check Wi-Fi connection
check_wifi()

# Connect to MQTT Broker
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(USER, PASSWORD)
client.connect(BROKER_ADDRESS, PORT)

# Configuration LED
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin_rfid, GPIO.OUT)
GPIO.output(led_pin_rfid, GPIO.LOW)
GPIO.setup(led_pin_tsl2561, GPIO.OUT)
GPIO.output(led_pin_tsl2561, GPIO.LOW)

data_thread = threading.Thread(target=read_tsl)
rfid_thread = threading.Thread(target=read_rfid)

data_thread.start()
rfid_thread.start()

# Loop
client.loop_start()

display_realtime_info()
