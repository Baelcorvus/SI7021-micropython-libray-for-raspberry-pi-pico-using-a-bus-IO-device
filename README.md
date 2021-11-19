# SI7021 micropython library for a raspberry pi pico using an I2C bus device
 Driver for the SI7021 - Temperature & Humidity Sensor in micropython using an I2C bus device for the raspberry pi pico microcontroller

Requires the presence of the I2C_bus_device librrary from:

https://github.com/Baelcorvus/I2C_Busdevice

The repository includes a version of the I2C bus device, the driver for the sensor and a couple of examples.
First you need to copy the files `SI7021.py` and `I2C_bus_device.py` from the repository to the default directory of you pico device.

To use call the object with the I2C bus to use and the address of the sensor.
If no address is given the default of 0x40 is used.

To use the device, first you must import the library:
 ```python
        from machine import Pin, I2C
        import SI7021
```
then define the I2C bus the device is attached to:
```python
        sdaPIN=machine.Pin(0)
        sclPIN=machine.Pin(1)
        i2c_bus = 0
        addr = 0x40

        i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)
```    
This will define an I2C bus on pin 0 for SDA and pin 1 for SCL. The actual pins will need to be changed
to the specifics of your project. The i2c_bus will be designated by the pins used. A pinout
of your pico will call the pins sda0 and scl0 for bus 0 and sda1 and scl1 for bus 1

to define the sensor object we then use:
```python
        si = SI7021.SI7021(i2c, addr)
```        
if the address is the same as the deafult the addr can be omited (so: `si = SI7021.SI7021(i2c)`
you can now use the sensore property .measurmenets to read the temperature and humidity.
You can then read the sesnore with the .measurments property. So:
```python
        temperature, humidity = sht..measurements
```        
The temperature and humdity can be read independently if required using the .temperature and
.relative_humidity properties:
```python
        temperature = si.temperature
        humidity = si.humidity
```
An example program is included that simply reads and prints these values (SI7021_example.py) and one that shows how you 
can integrate the sensor with other I2C bus devices.

```python
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
```

The other example is a simple program that incorportates this code into a multiple sensor situation.

***A note on I/O errors***
if an I/O error occuse durig either intialisation of the object or during a read of the sensor you can use `try:` and `except OSError:` 
to catch it and deal with it.
So, during intialisation we use:
```python
try:
    si = SI7021.SI7021(i2c, si_addr)
    serial, identifier = si._get_device_info()
except OSError:
    print ("SI7021 not present")
    si_attached = False
else:
    print('{} is present'.format(identifier))
```
The bus device responds with an error if no device is present with the address specified. If it finds a device at the address then you can read the chip identifier from the SI7021
with serial, identifier = si._get_device_info()`. The chip type will be returned in identifier.

Once we hace established a SI7021 device is present, future read and writes should occur without error, but in the case of a line dropping you can catch an error on a read:
```python
try:
    temperature, humidity = si.measurements         #read both temperature and humidity at the same time. 
    print("temperature: {}  Relative_humidity {}  ".format(temperature, humidity), end = '\r')
except OSError:      #if we get an error during I/O retry the connection
    temperature = 0
    humidity = 0
    print("SI7021 I/O Error - retrying connection")
```
Here if we get an I/O error reading the sensor we set the temperature and relative humidity values to 0 and complain about it. On the next loop the program will attempt to
read the device again.