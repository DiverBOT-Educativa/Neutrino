from orbit import ISS
from skyfield.api import load

t = load.timescale().now()

position = ISS.at(t)

location = position.subpoint()
print(location)
