import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# ——— Style settings ———
plt.rcParams['font.size']      = 20
plt.rcParams['axes.titlesize'] = 22
plt.rcParams['axes.labelsize'] = 22
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20

# ——— Script 1 data (CPU & Packets) ———
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

times_cpu  = np.linspace(0, 5, len(cpu_usage))
times_pkts = np.linspace(0, 5, len(packets_processed))
bar_width  = (times_cpu[1] - times_cpu[0]) * 0.8

# ——— Script 2 data (Throughput) ———
csv_data = """Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start
zero, 129515, 129515, 0, 1713, 14.0, 17.0, 20.0, 120.0, 210.0, 1744648003, 4129551387324060
zero, 254152, 254152, 0, 3449, 14.0, 18.0, 21.0, 143.0, 220.0, 1744648020, 4129593681262712
zero, 378915, 378915, 0, 5432, 13.0, 18.0, 21.0, 139.0, 222.0, 1744648038, 4129636553033392
zero, 503548, 503548, 0, 7879, 13.0, 19.0, 22.0, 159.0, 236.0, 1744648057, 4129680513452334
zero, 628245, 628245, 0, 11292, 12.0, 15.0, 21.0, 152.0, 222.0, 1744648076, 4129725750941037
zero, 753130, 753130, 0, 11781, 13.0, 19.0, 23.0, 184.0, 241.0, 1744648095, 4129772105164400
zero, 877810, 877810, 0, 15317, 11.0, 15.0, 19.0, 169.0, 240.0, 1744648115, 4129819866984288
zero, 1001739, 1001739, 0, 18272, 13.0, 19.0, 24.0, 199.0, 252.0, 1744648135, 4129868447885176
zero, 1126624, 1126624, 0, 23572, 12.0, 15.0, 18.0, 184.0, 242.0, 1744648156, 4129918532162397
zero, 1246922, 1246922, 0, 60290, 12.0, 17.0, 25.0, 207.0, 271.0, 1744648178, 4129969948457544
zero, 1368532, 1368532, 0, 88073, 12.0, 16.0, 21.0, 220.0, 255.0, 1744648199, 4130022062983059
zero, 1497659, 1497659, 0, 58007, 12.0, 16.0, 21.0, 231.0, 264.0, 1744648222, 4130075810689413
zero, 1501100, 1651100, 0, 263882, 12.0, 16.0, 23.0, 261.0, 301.0, 1744648245, 4130132155126428
zero, 1735129, 1735129, 0, 186716, 13.0, 16.0, 23.0, 217.0, 251.0, 1744648269, 4130188620989949
zero, 1878562, 1878562, 0, 930881, 13.0, 17.0, 41.0, 245.0, 273.0, 1744648293, 4130245561491750
zero, 1997182, 1997182, 0, 890229, 13.0, 17.0, 40.0, 233.0, 259.0, 1744648317, 41303036448233312
"""

# Read CSV with skipinitialspace to trim leading spaces in column names
df = pd.read_csv(StringIO(csv_data), skipinitialspace=True)

# Now 'Start' column exists without leading space
df['time']       = pd.to_datetime(df['Start'], unit='s')
df['delta_pkt']  = df['Actual'].diff()
df['delta_time'] = df['time'].diff().dt.total_seconds()
df['pps']        = df['delta_pkt'] / df['delta_time']
df = df.dropna(subset=['pps']).reset_index(drop=True)

t0 = df['time'].iloc[0]
df['minutes'] = ((df['time'] - t0).dt.total_seconds() / 60).round(1)

# Convert to Mbit/s
avg_pkt_bytes = 52
df['Mbps'] = df['pps'] * avg_pkt_bytes * 8 / 1e6

# Bar width for throughput
gap      = 0.4
min_step = df['minutes'].diff().min()
bw2      = gap * min_step

# ——— Create 2-row figure with shared X ———
fig, (ax1, ax2) = plt.subplots(
    nrows=2,
    ncols=1,
    sharex=True,
    figsize=(11, 10),
)

# --- Top: CPU & Packets ---
bars = ax1.bar(
    times_cpu, cpu_usage,
    width=bar_width,
    color='skyblue',
    label='CPU Usage (%)'
)
ax1.set_ylabel('CPU Usage (%)')
ax1.tick_params(labelbottom=False)  # hide X labels here

ax1b = ax1.twinx()
line_pkts, = ax1b.plot(
    times_pkts, packets_processed,
    marker='o', color='orange',
    label='Packets Processed'
)
ax1b.set_ylabel('Packets')

# Legend inside top-left
handles = [bars, line_pkts]
labels  = ['CPU Usage (%)','Packets Processed']
ax1.legend(handles, labels, loc='upper left')

# --- Bottom: Throughput Mbit/s ---
ax2.bar(
    df['minutes'], df['Mbps'],
    width=bw2,
    align='center',
    color='tab:green'
)
ax2.set_xlabel('Time (minutes)')
ax2.set_ylabel('Throughput (Mbit/s)')

plt.tight_layout()
plt.savefig("combined_two_plots.pdf")
