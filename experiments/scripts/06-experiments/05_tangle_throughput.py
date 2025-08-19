import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 24

# --------- raw data (unchanged) ----------
# csv_data = """Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
# zero, 129515, 129515, 0, 1713, 14.0, 17.0, 20.0, 120.0, 210.0, 1744648003, 4129551387324060
# zero, 254152, 254152, 0, 3449, 14.0, 18.0, 21.0, 143.0, 220.0, 1744648020, 4129593681262712
# zero, 378915, 378915, 0, 5432, 13.0, 18.0, 21.0, 139.0, 222.0, 1744648038, 4129636553033392
# zero, 503548, 503548, 0, 7879, 13.0, 19.0, 22.0, 159.0, 236.0, 1744648057, 4129680513452334
# zero, 628245, 628245, 0, 11292, 12.0, 15.0, 21.0, 152.0, 222.0, 1744648076, 4129725750941037
# zero, 753130, 753130, 0, 11781, 13.0, 19.0, 23.0, 184.0, 241.0, 1744648095, 4129772105164400
# zero, 877810, 877810, 0, 15317, 11.0, 15.0, 19.0, 169.0, 240.0, 1744648115, 4129819866984288
# zero, 1001739, 1001739, 0, 18272, 13.0, 19.0, 24.0, 199.0, 252.0, 1744648135, 4129868447885176
# zero, 1126624, 1126624, 0, 23572, 12.0, 15.0, 18.0, 184.0, 242.0, 1744648156, 4129918532162397
# zero, 1246922, 1246922, 0, 60290, 12.0, 17.0, 25.0, 207.0, 271.0, 1744648178, 4129969948457544
# zero, 1368532, 1368532, 0, 88073, 12.0, 16.0, 21.0, 220.0, 255.0, 1744648199, 4130022062983059
# zero, 1497659, 1497659, 0, 58007, 12.0, 16.0, 21.0, 231.0, 264.0, 1744648222, 4130075810689413
# zero, 1601100, 1601100, 0, 263882, 12.0, 16.0, 23.0, 261.0, 301.0, 1744648245, 4130132155126428
# zero, 1735129, 1735129, 0, 186716, 13.0, 16.0, 23.0, 217.0, 251.0, 1744648269, 4130188620989949
# zero, 1778562, 1778562, 0, 930881, 13.0, 17.0, 41.0, 245.0, 273.0, 1744648293, 4130245561491750
# zero, 1907182, 1907182, 0, 890229, 13.0, 17.0, 40.0, 233.0, 259.0, 1744648317, 41303036448233312
# """
csv_data = """Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
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

# --------- parameters ----------
average_pkt_size_bytes = 52 # default payload size is 24 bytes + UDP header (8 bytes) + IP header (20 bytes)

# --------- load & preprocess ----------
df = pd.read_csv(StringIO(csv_data.strip()), skipinitialspace=True)
df['time'] = pd.to_datetime(df['Start'], unit='s')

df['delta_actual'] = df['Actual'].diff()
df['delta_time_s'] = df['time'].diff().dt.total_seconds()
df['throughput_pps'] = df['delta_actual'] / df['delta_time_s']

plot_df = df.dropna(subset=['throughput_pps']).copy()
t0 = plot_df['time'].iloc[0]
plot_df['minutes'] = (
    (plot_df['time'] - t0).dt.total_seconds() / 60
).round(1)  # minutes since start

# ---- convert to networking-friendly units ----
plot_df['throughput_Mbps'] = plot_df['throughput_pps'] * average_pkt_size_bytes * 8 / 1e6
plot_df['throughput_Mpps'] = plot_df['throughput_pps'] / 1e6   # millions of pps (optional)

# --- plotting with gaps between bars ---
gap_factor = 0.4               # 0 = hair‑thin bars, 1 = bars touch
min_step   = plot_df['minutes'].diff().min()
bar_width  = gap_factor * min_step        # 60 % of the smallest interval

plot_df['throughput_Mbps_sm'] = (
    plot_df['throughput_Mbps']
    .rolling(window=3, min_periods=1, center=True)
    .mean()
)

# --------- plotting (Mb/s) ----------
plt.figure(figsize=(11, 8))
plt.bar(plot_df['minutes'],
        plot_df['throughput_Mbps_sm'],
        width=bar_width,    
        align='center')
# graph 05 - actual packets per seconds
# plt.bar(plot_df['minutes'],
#         plot_df['throughput_pps'],
#         edgecolor='black',
#         color='#0373fc',
#         width=bar_width,    
#         align='center')

# graph 05 - actual packets per seconds
plt.xlabel('Time (minutes)')
plt.ylabel('Throughput (Mbits/s)')
plt.title('')
plt.xticks(plot_df['minutes'].round(2))
plt.tight_layout()

# Save the plot to a file
plt.savefig("throughput_tangle_mbps.pdf")