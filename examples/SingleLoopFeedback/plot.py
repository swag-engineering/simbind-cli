# Before running the script install single_loop_feedback-10.0-py3-none-linux_x86_64.whl:
# pip install examples/SingleLoopFeedback/single_loop_feedback-10.0-py3-none-linux_x86_64.whl
# You will also need matplotlib:
# pip install matplotlib
# Then you can run the script:
# python examples/SingleLoopFeedback/plot.py



import matplotlib.pyplot as plt

from single_loop_feedback import Model


mod = Model()
data = {'time': [], 'input': [], 'output': []}

mod.input.speed_reference = 2000
while mod.time < 2:
    mod.step()
    data['time'].append(mod.time)
    data['input'].append(mod.input.speed_reference)
    data['output'].append(mod.output.out)

mod.input.speed_reference = 3000
while mod.time < 15:
    mod.step()
    data['time'].append(mod.time)
    data['input'].append(mod.input.speed_reference)
    data['output'].append(mod.output.out)

plt.plot(data['time'], data['input'], label='Input Speed Reference')
plt.plot(data['time'], data['output'], label='Output')
plt.xlabel('Time (s)')
plt.ylabel('Values')
plt.title('Single Loop Feedback')
plt.legend()
plt.show()
