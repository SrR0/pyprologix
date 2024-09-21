from pm2534 import pm2534
from time import sleep

port = "COM11"

test = pm2534(22, port, debug=True)
test.callReset()
#just a line added

#test.setDisplay("ADLERWEB.INFO")

print(test.getStatus())
print(test.getDigits(test.status.digits))
#print(test.getFunction(test.status.function))
#print(test.getRange(test.status.digits))
print(test.setFunction(test.Functions.RTW))
print(test.setTrigger(test.Triggers.K))
print(test.setDigits(3))
print(test.getDigits())
print(test.setRange(3E0))


#for x in range(6):

print(test.getMeasure())

#print(test.setRange("A"))
#print(test.setDigits(5))

#test.getCalibration("calibration.data")
