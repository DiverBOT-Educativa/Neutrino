from orbit import ISS
import time
while True:
    location = ISS.coordinates() # Equivalent to ISS.at(timescale.now()).subpoint()
    print(f'Latitude: {location.latitude}')
    print(f'Longitude: {location.longitude}')
    print(f'Elevation: {location.elevation.km}')
    time.sleep(0.5)
