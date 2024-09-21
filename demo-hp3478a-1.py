
from hp3478a import hp3478a
from time import sleep

port = "COM12"

test = hp3478a(23, port, debug=False)

#test.callReset()
"""
test.setDisplay("ADLERWEB.INFO")
print(test.getStatus())
print(test.getDigits(test.status.digits))
print(test.getFunction(test.status.function))
print(test.getRange(test.status.digits))
"""
print(test.setFunction(test.Ω2W))
print(test.setTrigger(test.TRIG_INT))
print(test.setRange("300"))
#print(test.setDigits(3.5))

#for x in range(6):

print(test.getMeasure())

#print(test.setRange("A"))
#print(test.setDigits(5))

#test.getCalibration("calibration.data")
