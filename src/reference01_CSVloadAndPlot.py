import easygui
import pandas as pd
import matplotlib.pyplot as plt

fileName = easygui.fileopenbox(msg="Choose a file", default=r"radiosignal.csv")
data = pd.read_csv(fileName, sep=',', delimiter=None, header='infer', names=None, index_col=None)

time = data['time'].tolist()
#time = time[0:(len(time)-4)]

signal = data['signal'].tolist()
#signal = signal[0:(len(signal)-4)]

fig, axs = plt.subplots(2, 1, sharex=True, sharey=False)
fig.suptitle('time - signal')
axs[0].plot(time, signal, label="signal")
axs[0].grid()
axs[0].set_xlabel("time (ms)")
axs[0].set_ylabel("signal")
plt.show()