# Before running the script install antiwindup_controller-5.0-py3-none-linux_x86_64.whl:
# pip install examples/AntiWindupPidController/antiwindup_controller-5.0-py3-none-linux_x86_64.whl
# You will also need matplotlib:
# pip install matplotlib
# Then you can run the script:
# python examples/AntiWindupPidController/plot.py

import matplotlib.pyplot as plt

from antiwindup_controller import Model


mod = Model()
data = {'time': [], 'input': [], 'output': []}

mod.input.rt = 10
while mod.time < 80:
    mod.step()
    data['time'].append(mod.time)
    data['input'].append(mod.input.rt)
    data['output'].append(mod.output.yout)

mod.input.rt = 5
while mod.time < 200:
    mod.step()
    data['time'].append(mod.time)
    data['input'].append(mod.input.rt)
    data['output'].append(mod.output.yout)

plt.plot(data['time'], data['input'], label='r(t)')
plt.plot(data['time'], data['output'], label='y(t)')
plt.xlabel('Time (s)')
plt.ylabel('Values')
plt.title('Anti-Windup Control Using PID Controller')
plt.legend()
plt.show()
