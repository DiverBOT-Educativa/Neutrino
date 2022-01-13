import pisense
from sense_hat import SenseHat
sense = SenseHat()
sense.clear

magnetometer = pisense.SenseIMU(settings=None , emulate=False)
print(magnetometer.compass)
