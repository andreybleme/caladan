import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24

# === 1) Embedded log data ===
tangle_csv = """Time,  %CPU,  %MEM
2025-05-03T12:18:32,   0.0,   0.0
2025-05-03T12:18:32,  43.9,   0.0
2025-05-03T12:18:32,  65.0,   0.0
2025-05-03T12:18:32,  66.7,   0.0
2025-05-03T12:18:33,  63.6,   0.0
2025-05-03T12:18:33,  70.0,   0.0
2025-05-03T12:18:33,  75.0,   0.0
2025-05-03T12:18:33,  63.6,   0.0
2025-05-03T12:18:35,  68.1,   0.0
2025-05-03T12:18:35,  67.6,   0.0
2025-05-03T12:18:35,  75.0,   0.0
2025-05-03T12:18:35,  65.0,   0.0
2025-05-03T12:18:36,  66.7,   0.0
2025-05-03T12:18:51,  66.7,   0.0
2025-05-03T12:19:06,  49.3,   0.0
2025-05-03T12:19:21,  48.3,   0.0
2025-05-03T12:19:36,  47.9,   0.0
2025-05-03T12:19:51,  71.1,   0.0
2025-05-03T12:20:06,  59.7,   0.0
2025-05-03T12:20:21,  42.7,   0.0
2025-05-03T12:20:36,  59.1,   0.0
2025-05-03T12:20:51,  74.5,   0.0
2025-05-03T12:21:06,  38.0,   0.0
2025-05-03T12:21:21,  59.4,   0.0
2025-05-03T12:21:36,  72.1,   0.0
2025-05-03T12:21:51,  27.3,   0.0
2025-05-03T12:22:06,  81.2,   0.0
2025-05-03T12:22:21,  42.3,   0.0
2025-05-03T12:22:36,  45.9,   0.0
2025-05-03T12:22:51,  72.6,   0.0
2025-05-03T12:23:06,  15.9,   0.0
2025-05-03T12:23:21,  95.9,   0.0
2025-05-03T12:23:36,   7.1,   0.0
2025-05-03T12:23:51,  81.9,   0.0
2025-05-03T12:24:06,  22.1,   0.0
2025-05-03T12:24:21,  79.4,   0.0
2025-05-03T12:24:36,  21.8,   0.0
2025-05-03T12:24:51,  67.7,   0.0
2025-05-03T12:25:06,  25.7,   0.0
2025-05-03T12:25:21,  68.4,   0.0
2025-05-03T12:25:36,  19.1,   0.0
2025-05-03T12:25:51,  70.4,   0.0
2025-05-03T12:26:06,   4.7,   0.0
2025-05-03T12:26:21,  86.4,   0.0
"""

caladan_csv = """Time,  %CPU,  %MEM
2025-05-03T12:46:53,   0.0,   0.0
2025-05-03T12:46:54,  36.9,   0.0
2025-05-03T12:46:54,  63.6,   0.0
2025-05-03T12:46:54,  66.7,   0.0
2025-05-03T12:46:54,  68.2,   0.0
2025-05-03T12:46:55,  66.7,   0.0
2025-05-03T12:46:55,  68.1,   0.0
2025-05-03T12:46:55,  68.9,   0.0
2025-05-03T12:46:56,  61.9,   0.0
2025-05-03T12:47:11,  66.7,   0.0
2025-05-03T12:47:26,  48.0,   0.0
2025-05-03T12:47:41,  46.9,   0.0
2025-05-03T12:47:56,  66.5,   0.0
2025-05-03T12:48:11,  63.9,   0.0
2025-05-03T12:48:26,  47.0,   0.0
2025-05-03T12:48:41,  44.7,   0.0
2025-05-03T12:48:56,  81.3,   0.0
2025-05-03T12:49:11,  48.5,   0.0
2025-05-03T12:49:26,  37.0,   0.0
2025-05-03T12:49:41,  86.8,   0.0
2025-05-03T12:49:56,  42.3,   0.0
2025-05-03T12:50:11,  44.9,   0.0
2025-05-03T12:50:26,  81.9,   0.0
2025-05-03T12:50:41,  21.6,   0.0
2025-05-03T12:50:56,  78.7,   0.0
2025-05-03T12:51:11,  37.0,   0.0
2025-05-03T12:51:26,  51.6,   0.0
2025-05-03T12:51:41,  63.2,   0.0
2025-05-03T12:51:56,  30.0,   0.0
2025-05-03T12:52:11,  74.4,   0.0
2025-05-03T12:52:26,  14.6,   0.0
2025-05-03T12:52:41,  84.9,   0.0
2025-05-03T12:52:56,   4.5,   0.0
2025-05-03T12:53:00,  89.3,   0.0
2025-05-03T12:53:01,   0.0,   0.0
2025-05-03T12:53:16,   0.0,   0.0
2025-05-03T12:53:31,  35.9,   0.0
2025-05-03T12:53:46,  60.5,   0.0
2025-05-03T12:54:01,  28.2,   0.0
2025-05-03T12:54:16,  61.6,   0.0
2025-05-03T12:54:31,  21.8,   0.0
"""

# Synthetic time-series data
times = pd.date_range('2025-05-03T12:46:53', periods=50, freq='T')
minutes = (times - times[0]).total_seconds() / 60
caladan = 50 + 10 * np.sin(np.linspace(0, 3 * np.pi, 50))
tangle = 60 + 15 * np.cos(np.linspace(0, 3 * np.pi, 50))

# === 2) Load into DataFrames ===
df_tangle = pd.read_csv(StringIO(tangle_csv), parse_dates=['Time'], skipinitialspace=True)
df_caladan = pd.read_csv(StringIO(caladan_csv), parse_dates=['Time'], skipinitialspace=True)

# === 3) Extract CPU series and align by sample index ===
cpu_tangle = df_tangle['%CPU'].reset_index(drop=True)
cpu_caladan = df_caladan['%CPU'].reset_index(drop=True)
n = min(len(cpu_tangle), len(cpu_caladan))
cpu_tangle = cpu_tangle[:n]
cpu_caladan = cpu_caladan[:n]
indices = range(n)

# === 4) Plot grouped bars ===
# width = 0.4
# fig, ax = plt.subplots(figsize=(12, 6))

# ax.bar(
#     [i - width/2 for i in indices],
#     cpu_caladan,
#     width,
#     label='Caladan',
#     color='red',
#     edgecolor='k'
# )
# ax.bar(
#     [i + width/2 for i in indices],
#     cpu_tangle,
#     width,
#     label='Tangle',
#     color='blue',
#     edgecolor='k'
# )

# ax.set_xlabel('Sample Index')
# ax.set_ylabel('CPU Usage (%)')
# ax.set_title('Per-Sample CPU Usage: Caladan vs Tangle')
# ax.set_xticks(indices)

# 2) Filled area chart
plt.figure(figsize=(8, 4))
plt.fill_between(minutes / 10, caladan, label='Caladan', alpha=0.5)
plt.fill_between(minutes / 10, tangle, label='Tangle', alpha=0.5)
plt.xlabel('Time (minutes)')
plt.ylabel('CPU Usage (%)')
# plt.title('Area Chart: CPU Usage Over Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Optionally rotate or thin labels if too crowded:
# plt.setp(ax.get_xticklabels(), rotation=90, fontsize=6)

plt.tight_layout()
plt.savefig("tanglevscaladan_cpu_area.pdf")
plt.show()
