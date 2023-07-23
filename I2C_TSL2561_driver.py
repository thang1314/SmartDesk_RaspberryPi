import smbus
import time

# TSL2561 I2C address
TSL2561_ADDR = 0x39

# Initialize I2C bus (you may need to adjust the bus number)
bus = smbus.SMBus(1)

# Function to read a 16-bit value from the TSL2561 sensor
def read_word(register):
    low_byte = bus.read_byte_data(TSL2561_ADDR, register)
    high_byte = bus.read_byte_data(TSL2561_ADDR, register + 1)
    return (high_byte << 8) + low_byte

# Read Full Spectrum, Visible, and Infrared values from TSL2561
def read_tsl2561():
    # Power on the TSL2561 sensor
    bus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)

    # Wait for integration time (adjust this according to your sensor's integration time)
    time.sleep(0.5)

    # Read Full Spectrum, Visible, and Infrared data
    full_spectrum = read_word(0x8D)
    visible = read_word(0x8C) - read_word(0x8E)
    infrared = read_word(0x8E)

    # Power off the TSL2561 sensor
    bus.write_byte_data(TSL2561_ADDR, 0x80, 0x00)

    return full_spectrum, visible, infrared

# # Read TSL2561 sensor data
# full_spectrum, visible, infrared = read_tsl2561()

# # Print Full Spectrum, Visible, and Infrared values
# #print("Full Spectrum: ", full_spectrum)
# print("Visible: ", visible)
# print("Infrared: ", infrared)
