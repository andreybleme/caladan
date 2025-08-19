import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Use the user's style settings
plt.rcParams['font.size']      = 20
plt.rcParams['axes.titlesize'] = 22
plt.rcParams['axes.labelsize'] = 22
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20

# Provided data
cpu_usage = [
    43.9, 45.0, 46.7, 43.6, 70.0, 75.0, 63.6, 68.1, 67.6, 75.0, 65.0,
    66.7, 66.7, 49.3, 48.3, 47.9, 71.1, 59.7, 42.7, 59.1, 74.5, 38.0,
    59.4, 72.1, 27.3, 81.2, 42.3, 45.9, 72.6, 15.9, 95.9,  7.1, 81.9,
    22.1, 79.4, 21.8, 67.7, 25.7, 68.4, 19.1, 70.4,  4.7, 86.4
]
packets_processed = [
    603955, 803477, 1001175, 1249629, 1600565,
    1817890, 1973209, 2089455, 2099455
]

# Evenly space data over 0–5 minutes
times_cpu  = np.linspace(0, 5, len(cpu_usage))
times_pkts = np.linspace(0, 5, len(packets_processed))

bar_width = (times_cpu[1] - times_cpu[0]) * 0.8

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 6))

# Plot CPU bars
bars = ax.bar(
    times_cpu,
    cpu_usage,
    width=bar_width,
    color='skyblue',
    align='center',
    label='CPU'
)
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('CPU Usage (%)')

# Plot packets line on secondary axis
ax2 = ax.twinx()
line, = ax2.plot(
    times_pkts,
    packets_processed,
    marker='o',
    color='orange',
    label='Packets',
)
ax2.set_ylabel('Packets (millions)')

# Place legend inside the plot at top left
handles = [bars, line]
labels = ['CPU', 'Packets']
ax.legend(handles, labels, loc='upper left')

plt.title('')
plt.tight_layout()
plt.savefig("tangle_cpuvspackets.pdf")
