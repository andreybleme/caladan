import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 24

csv_data = """Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 129606, 129606, 0, 1721, 14.0, 17.0, 19.0, 116.0, 209.0, 1761045752, 36530909127421260
zero, 254076, 254076, 0, 3499, 14.0, 18.0, 21.0, 134.0, 216.0, 1761045770, 36530951309101528
zero, 378595, 378595, 0, 5261, 13.0, 18.0, 20.0, 147.0, 227.0, 1761045788, 36530993750933424
zero, 503273, 503273, 0, 7037, 12.0, 18.0, 21.0, 157.0, 235.0, 1761045805, 36531036457318940
zero, 627898, 627898, 0, 8635, 11.0, 16.0, 20.0, 152.0, 229.0, 1761045822, 36531079413920745
zero, 752278, 752278, 0, 10578, 11.0, 16.0, 21.0, 158.0, 233.0, 1761045840, 36531122734042416
zero, 877088, 877088, 0, 12699, 11.0, 17.0, 22.0, 167.0, 236.0, 1761045860, 36531166742711560
zero, 1001484, 1001484, 0, 14471, 11.0, 16.0, 22.0, 171.0, 239.0, 1761045878, 36531211111227462
zero, 1127397, 1127397, 0, 16765, 11.0, 15.0, 22.0, 181.0, 247.0, 1761045897, 36531256424024541
zero, 1251283, 1251283, 0, 18237, 11.0, 15.0, 21.0, 187.0, 249.0, 1761045914, 36531302554726038
zero, 1375874, 1375874, 0, 20535, 12.0, 15.0, 19.0, 199.0, 255.0, 1761045933, 36531349070270631
zero, 1501293, 1501293, 0, 22128, 12.0, 15.0, 20.0, 209.0, 261.0, 1761045948, 36531396247339920
zero, 1624878, 1624878, 0, 24500, 12.0, 15.0, 20.0, 202.0, 263.0, 1761045973, 36531444493003389
zero, 1751480, 1751480, 0, 26450, 12.0, 16.0, 20.0, 211.0, 271.0, 1761045994, 36531493291495044
zero, 1875256, 1875256, 0, 29105, 13.0, 16.0, 21.0, 212.0, 267.0, 1761046012, 36531542277199164
zero, 1999076, 1999076, 0, 32124, 13.0, 17.0, 22.0, 222.0, 271.0, 1761046031, 36531592119048834
zero, 2123854, 2123854, 0, 35006, 14.0, 18.0, 32.0, 240.0, 326.0, 1761046053, 36531642501831795
zero, 2249592, 2249592, 0, 35711, 14.0, 18.0, 25.0, 262.0, 351.0, 1761046074, 36531693700787715
zero, 2371397, 2371397, 0, 40311, 15.0, 19.0, 28.0, 230.0, 381.0, 1761046093, 36531745587180882
zero, 2496908, 2496908, 0, 44641, 16.0, 22.0, 80.0, 266.0, 416.0, 1761046115, 36531798192133632
"""

# --------- parameters ----------
average_pkt_size_bytes = 52  # default payload size is 24 bytes + UDP header (8 bytes) + IP header (20 bytes)

# --------- load & preprocess ----------
df = pd.read_csv(StringIO(csv_data.strip()), skipinitialspace=True)
df['time'] = pd.to_datetime(df['Start'], unit='s')

df['delta_actual'] = df['Target'].diff()
df['delta_time_s'] = df['time'].diff().dt.total_seconds()
df['throughput_pps'] = df['delta_actual'] / df['delta_time_s']

plot_df = df.dropna(subset=['throughput_pps']).copy()
t0 = plot_df['time'].iloc[0]
plot_df['minutes'] = (
    (plot_df['time'] - t0).dt.total_seconds() / 60
).round(1)  # minutes since start

# ---- convert to networking-friendly units ----
plot_df['throughput_Mbps'] = plot_df['throughput_pps'] * average_pkt_size_bytes * 8 / 1e6

# --- plotting with gaps between bars ---
gap_factor = 0.7               # 0 = hair-thin bars, 1 = bars touch
min_step   = plot_df['minutes'].diff().min()
bar_width  = gap_factor * min_step        # 60 % of the smallest interval

# smooth Mbps as before
plot_df['throughput_Mbps_sm'] = (
    plot_df['throughput_Mbps']
    .rolling(window=3, min_periods=1, center=True)
    .mean()
)

# --------- plotting with dual Y axis ----------
fig, ax1 = plt.subplots(figsize=(11, 8))

# Bars in Mbits/s (left axis) – same visual style as your first script
ax1.bar(
    plot_df['minutes'],
    plot_df['throughput_Mbps_sm'],
    width=bar_width,
    align='center'
)
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Throughput (Mbits/s)')
ax1.set_title('')
ax1.set_xticks(plot_df['minutes'].round(2))

# two-iok: copilot - only show every other x label to avoid crowding
xtick_labels = [str(x) if i % 2 == 0 else "" for i, x in enumerate(plot_df['minutes'].round(2))]
ax1.set_xticklabels(xtick_labels)

# Right Y axis in packets per second (pps), sharing the same underlying data
ax2 = ax1.twinx()
ax2.set_ylabel('Packets per second (pps)')

# Conversion: Mbps -> pps
# Mbps = pps * (bytes_per_pkt * 8) / 1e6
# => pps = Mbps * 1e6 / (bytes_per_pkt * 8)
conversion_factor = 1e6 / (average_pkt_size_bytes * 8)

ymin, ymax = ax1.get_ylim()
ax2.set_ylim(ymin * conversion_factor, ymax * conversion_factor)

fig.tight_layout()

# Save the plot to a file
plt.savefig("throughput_tangle_combined_mbps_pps.pdf")
plt.show()
