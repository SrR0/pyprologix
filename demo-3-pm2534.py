from pm2534 import pm2534
from time import sleep

port = "COM11"

test = pm2534(23, port, debug=True)
#test.callReset()
"""
test.setDisplay("ADLERWEB.INFO")
print(test.getStatus())
print(test.getDigits(test.status.digits))
print(test.getFunction(test.status.function))
print(test.getRange(test.status.digits))
print(test.setFunction(test.Ω2W))
print(test.setTrigger(test.TRIG_INT))
print(test.setRange("300"))
#print(test.setDigits(3.5))

for x in range(6):
"""
print(test.getMeasure())

#print(test.setRange("A"))
#print(test.setDigits(5))

#test.getCalibration("calibration.data")
