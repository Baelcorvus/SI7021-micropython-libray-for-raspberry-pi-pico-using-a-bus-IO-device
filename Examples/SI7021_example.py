'''
Code to use a SHTC3 - Temperature & Humidity Sensor with a pico microcontroller
in micropython using an I2C bus device.
'''

'''first we import the libraries'''
from machine import Pin, I2C
from time import sleep
import SI7021

'''Then we define the physical I2C that the sensor is connected to''' 
sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
i2c_bus = 0

i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)

si_addr = 0x40

'''and finnaly set up the sensor object that will always talk to the sensor'''

try:
    si = SI7021.SI7021(i2c, si_addr)
    serial, identifier = si._get_device_info()
except OSError:
    print ("SI7021 not present")
    si_attached = False
else:
    print('{} is present'.format(identifier))
    
while True:
    try:
        temperature, humidity = si.measurments         #read both temperature and humidity at the same time. 
        print("temperature: {}  Relative_humidity {}  ".format(temperature, humidity), end = '\r')
    except OSError:      #if we get an error during I/O retry the connection
        temperature = 0
        humidity = 0
        print("SHTC3 I/O Error - retrying connection")

    sleep(0.1)                                           #read every half second - not necessary for the bus, just cosmetic, omit as needed