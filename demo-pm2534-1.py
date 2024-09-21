import time

from pm2534 import pm2534
from time import sleep

port = "COM11"

test = pm2534(22, port, debug=True)
test.callReset()
#just a line added

#test.setDisplay("ADLERWEB.INFO")

print(test.getStatus())
#print(test.getDigits(test.status.digits))
#print(test.getFunction(test.status.function))
#print(test.getRange(test.status.digits))
print(test.setFunction(test.Functions.VDC))
#print(test.setTrigger(test.Triggers.K))
print(test.setSpeed(test.Speeds.Speed1))
#print(test.getDigits())
print(test.setRange(30E0))

for x in range(100):
    print(test.getMeasure())
    time.sleep(3)

#print(test.setRange("A"))
#print(test.setDigits(5))

#test.getCalibration("calibration.data")
