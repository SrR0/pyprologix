import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from hp3478a import hp3478a
from time import sleep, time
# Initialize the connection and measurement parameters for the multimeter
port="COM11"
test = hp3478a(23, port, debug=False)

test.callReset()

test.setDisplay("ADLERWEB.INFO")
print(test.getStatus())
print(test.getDigits(test.status.digits))
print(test.getFunction(test.status.function))
print(test.getRange(test.status.digits))
print(test.setFunction(test.Ω2W))
print(test.setTrigger(test.TRIG_INT))
print(test.setRange("300"))
#print(test.setDigits(3.5))
# Lists for storing the time and measurement values
times = []
measurements = []
# Function to get data from the multimeter
def get_measurement():
    return float(test.getMeasure())
# Function to update the graph
def update(frame):
    current_time = time()
    measurement = get_measurement()
    print(measurement)
    times.append(current_time)
    measurements.append(measurement)
    ax.clear()
    ax.plot(times, measurements)
    ax.set(xlabel='Time (s)', ylabel='Measurement (Ohms)',
           title='Multimeter Measurements Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
# Setup the plot
fig, ax = plt.subplots()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Measurement (Ohms)')
ax.set_title('Multimeter Measurements Over Time')
# Animation function calls update every 10000 ms (10 seconds)
ani = FuncAnimation(fig, update, interval=3000)
# Display the plot
plt.show()
