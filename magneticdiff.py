import geomag
import pisense
import math
from orbit import ISS

sense_imu = pisense.SenseIMU()
gm = geomag.GeoMag()

def compass_module():
    # Get the length of the compass' three axes vector
    compass = sense_imu.read().compass
    return math.sqrt(math.pow(compass.x, 2) + math.pow(compass.y, 2) + math.pow(compass.z, 2))
def geomag_module():
    # Get the length of the geomag three axes vector
    location = ISS.coordinates()
    mag = gm.GeoMag(location.latitude.degrees, location.longitude.degrees, location.elevation.m)
    return math.sqrt(math.pow(mag.bx / 1000, 2) + math.pow(mag.by / 1000, 2) + math.pow(mag.bz / 1000, 2))
def module_relation():
    # Divide between the two modules
    module_gm = geomag_module()
    module_compass = compass_module()
    return module_gm/module_compass

def calibrate():
    # Get the average of 'precision' module_relation()
    precision = 1000
    average = 0
    for i in range(precision):
        average += module_relation()
    return average / precision

def magnetic_deviation(relation):
    # Get the difference between what the compass measures times the average relation
    # and the geomag values
    mag = geomag_module()
    expected_value = compass_module() * relation
    return expected_value - mag

def fill_buffer(buffer, relation):
    for i in range(1000):
        buffer[i] = magnetic_deviation(relation)

def avg_deviation(buffer, relation):
    buffer.pop()
    buffer.insert(0, magnetic_deviation(relation))
    sensor_avg = 0
    for reading in buffer:
        sensor_avg += reading
    return sensor_avg / len(buffer)
