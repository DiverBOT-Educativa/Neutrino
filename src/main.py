import geomag
import os
from datetime import date
import csv
from pisense import SenseHat
from datetime import datetime
from pathlib import Path
from time import sleep
from orbit import ISS
from skyfield.api import load

sense = SenseHat()
base_folder = Path(__file__).parent.resolve()
data_file = open("{}/data.csv".format(base_folder), buffering=1)
csv_writer = csv.writer(csv_writer)

headers = ("Date/Time", "Magnetometer", "Location", "Accelerometer", "Humidity", "AtmPressure", "Temperature", "Gyroscope")
csv_writer.writerow(headers)

for i in range(0, 1000):
    csv_writer.writerow((datetime.now(), sense.imu.compass, ISS.at(load.timescale().now()), sense.imu.accel, sense.environ.humidity, sense.environ.pressure, sense.environ.temperature, sense.imu.gyro))
    sleep(1000)

#https://wheretheiss.at/

gm = geomag.GeoMag()
mag = gm.GeoMag(29,32,400, )
