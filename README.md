# SmartDesk_RaspberryPi

## Installation

Before we start programming, we first need to update our Raspberry Pi to ensure it’s running the latest version of all the software. Run the following two commands on your Raspberry Pi to update it.

```
sudo apt update
sudo apt upgrade
```

Install python3-dev, python-pip and  git packages
```
sudo apt-get install python3-dev python3-pip
```

### RFID

Before we get started programming, make sure the SPI interface is enabled on your Raspberry Pi.
Install MFRC522 library:
```
sudo apt-get -y install python3-pip
sudo pip install mfrc522
```

### LCD and TSL2561
Before we get started programming, make sure the I2C interface is enabled on your Raspberry Pi.
Install I2C-TOOLS and SMBUS
```
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
```

### Pi Camera
Before we get started programming, make sure the camera is enabled on your Raspberry Pi.
Install SocketIO library:
```
sudo pip install python-socketio
```

