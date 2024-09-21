import sdm3065x

dmm = sdm3065x.SDM3065X('10.0.0.114')
dmm.reset()

# setup:
v = dmm.getVoltageDC('20V', 0.05)  # set NPLC to 0.05 which is 1ms in a 50Hz grid
print(v)

# further readings:
for i in range(10):
    print(dmm.read())