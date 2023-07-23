# SmartDesk_RaspberryPi
## Introduce
Project "SmartDesk_RaspberryPi" build an intelligent smart desk system using an IoT platform, incorporating microcontrollers Raspberry Pi and peripherals such as a camera, clock, light sensor, etc. 

## How it works
This part is related to the hardware aspect.

Raspberry Pi communicates with peripheral devices (RFID-RC522, TSL2561, Pi camera, LCD 16x2) and collects data from them.

- Display real-time infomation: Display on LCD 16x2 through I2C communication.

- Streaming: The Pi camera reads frames from the camera and then stores them as binary streams. It sends these streams to the server through a socket.io connection.

- Light condition monitoring: Using the TSL2561 light sensor connected to the microcontroller, communicated via I2C. The TSL2561 sensor is used to monitor ambient light conditions. The system may automatically turn on or turn off the desk's LED light based on the surrounding light intensity to provide optimal illumination. This feature ensures that the LED light is only activated when needed, saving energy and creating a comfortable learning environment for students.

- Card scanning function: Utilizing RFID RC522 to connect to the microcontroller via SPI communication. The RC522 is employed for attendance tracking using RFID cards or tags. When a student wants to register their attendance, they can simply tap their RFID card or tag near the RC522 reader. The RC522 module, interfaced with Raspberry Pi, scans the card and reads its unique identification number.

- All data collected from modules and sensors like RFID-RC522, TSL2561 is transmitted to the server through MQTT Broker.

## Installation
Before we start programming, we first need to update our Raspberry Pi to ensure it’s running the latest version of all the software. Run the following two commands on your Raspberry Pi to update it.
```
sudo apt update
sudo apt upgrade
```
Make sure the SPI, I2C interface and camera are enabled on your Raspberry Pi.
Remember to install the necessary libraries by running the following commands in your terminal if you haven't already done so:
### python3-dev, python-pip and  git packages
```
sudo apt-get install python3-dev python3-pip
```
### RFID-MFRC522 library:
```
sudo apt-get -y install python3-pip
sudo pip install mfrc522
```
### I2C-tools and SMBus:
```
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
```
### SocketIO library:
```
sudo pip install python-socketio
```
### Paho-mqtt
```
pip install paho-mqtt
```
