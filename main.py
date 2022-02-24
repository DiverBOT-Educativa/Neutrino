import csv
from sense_hat import SenseHat 
from datetime import datetime, timedelta
from pathlib import Path
#from time import datetime, date, timedelta
from orbit import ISS
from skyfield.api import load
import magneticdiff
import logging

logFile = "Errors.log"

logging.basicConfig(filename=logFile, level=logging.DEBUG, format="") # No format (to print header)
logging.info("=== Neutrino LOGS ===") # Print header
logging.info(f"Started at {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}") # Print start time
logging.info("") # Print an empty line

# Remove all logging handlers, so we can run logging.basicConfig() again
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Define main format
logging.basicConfig(filename=logFile, level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

start_time = datetime.now()
now_time = datetime.now()

sense = SenseHat() #sense object to read sensors of SenseHat board

base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'

totalLines = 0 # to count the lines written in the csv file
goodLines = 0  # to cound the amount of good data stored


# Initialize the magnetic difference module
mg_relation = magneticdiff.calibrate()
buffer = [None] * 1000 # Buffer used to average measurements
magneticdiff.fill_buffer(buffer, mg_relation)

with open(data_file, 'a', buffering=1) as f:
    logging.info('The file data.csv has been opened')
    writer = csv.writer(f)
    while (now_time < start_time + timedelta(minutes=176)):
        fecha = datetime.now()
        location = ISS.coordinates()  
        try:
            # Get the values from the magnetometer, accelerometer and gyroscope
            xOri, yOri, zOri = sense.orientation.values()
            xAcc, yAcc, zAcc = sense.accelerometer.values()
            xCom, yCom, zCom = sense.compass_raw.values()

            # Writing on the file all the info we have get from sensors
            row = (fecha.strftime('%Y-%m-%d'), fecha.strftime('%H:%M:%S:%s'), sense.humidity, sense.temperature, sense.pressure, xOri, yOri, zOri, xAcc, yAcc, zAcc, xCom, yCom, zCom, location.latitude.degrees, location.longitude.degrees)
            goodLines += 1

            # Check the magnetic field
            mg_deviation = magneticdiff.avg_deviation(buffer, mg_relation)

            if mg_deviation >= 1 or mg_deviation <= -1:
                sense.clear(128, 0, 0) # There is a magnetic anomaly so red screen
            else:
                sense.clear(0, 128, 0) # Everything is ok, green screen

        except Exception: 
             logging.exception("Error while trying to read")
             # As an error has ocurred, we will write an empty line
             row = (fecha.strftime('%Y-%m-%d'), fecha.strftime('%H:%M:%S:%s'), '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-')
        
        writer.writerow(row)
        totalLines += 1

        # wait exactly 1 second since last data
        while(now_time < fecha + timedelta(seconds = 1)):
            now_time = datetime.now()
        now_time = datetime.now()
    
    # print some lines on the log file
    logging.info('The time has expired')
    lapsedTime = datetime.now()-start_time
    logging.info('The data collection has last for {} minutes'.format(lapsedTime.seconds / 60))
    logging.info('Total lines added to data.csv = {} , from which {} contain good data'.format(totalLines,goodLines))
        
logging.info('The file data.csv has been closed')
