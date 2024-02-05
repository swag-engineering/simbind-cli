# Before running the script install flight_controller-6.0-py3-none-linux_x86_64.whl:
# pip install examples/LongitudinalFlightControl/flight_controller-6.0-py3-none-linux_x86_64.whl
# You will also need matplotlib:
# pip install matplotlib
# Then you can run the script:
# python examples/LongitudinalFlightControl/plot.py

import matplotlib.pyplot as plt

from flight_controller import Model


mod = Model()
data = {'time': [], 'input': [], 'output': []}

while mod.time < 10:  # Simulate for 10 seconds
    # Switch input value every three seconds
    if int(mod.time) % 6 < 3:
        mod.input.stick = 0.5
    else:
        mod.input.stick = -0.5

    mod.step()  # Iterate over time
    # Store data
    data['time'].append(mod.time)
    data['input'].append(mod.input.stick)
    data['output'].append(mod.output.alpharad)

plt.plot(data['time'], data['input'], label='Stick')
plt.plot(data['time'], data['output'], label='Alpha')
plt.xlabel('Time (s)')
plt.ylabel('Values')
plt.title('Aircraft Longitudinal Flight Control')
plt.legend()
plt.show()
