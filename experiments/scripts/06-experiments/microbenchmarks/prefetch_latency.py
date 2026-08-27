import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24

# Log data as a multiline string
log_data = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 129700, 129700, 0, 1850, 14.0, 17.0, 20.0, 122.0, 208.0, 1761048248, 36536885291535592
zero, 253980, 253980, 0, 3591, 14.0, 18.0, 20.0, 128.0, 214.0, 1761048266, 36536927491839712
zero, 378369, 378369, 0, 5185, 13.0, 18.0, 20.0, 151.0, 226.0, 1761048284, 36536970023671792
zero, 503156, 503156, 0, 6848, 12.0, 17.0, 20.0, 148.0, 226.0, 1761048301, 36537012816236352
zero, 628168, 628168, 0, 8527, 11.0, 17.0, 21.0, 152.0, 231.0, 1761048319, 36537055817970636
zero, 752776, 752776, 0, 10302, 11.0, 16.0, 21.0, 154.0, 229.0, 1761048337, 36537099125860521
zero, 876724, 876724, 0, 12258, 11.0, 16.0, 22.0, 166.0, 237.0, 1761048356, 36537143076356040
zero, 1001827, 1001827, 0, 14404, 11.0, 16.0, 22.0, 170.0, 240.0, 1761048374, 36537187526611182
zero, 1126366, 1126366, 0, 16162, 11.0, 16.0, 23.0, 183.0, 249.0, 1761048393, 36537232630341144
zero, 1251250, 1251250, 0, 18201, 11.0, 15.0, 19.0, 184.0, 250.0, 1761048412, 36537278777453946
zero, 1375746, 1375746, 0, 20126, 12.0, 15.0, 19.0, 199.0, 255.0, 1761048432, 36537325375989750
zero, 1500858, 1500858, 0, 22073, 12.0, 15.0, 20.0, 207.0, 259.0, 1761048452, 36537372339096594
zero, 1625115, 1625115, 0, 24375, 12.0, 15.0, 20.0, 202.0, 262.0, 1761048472, 36537420432514920
zero, 1749980, 1749980, 0, 26502, 12.0, 16.0, 21.0, 208.0, 267.0, 1761048492, 36537469091099892
zero, 1875350, 1875350, 0, 29213, 13.0, 16.0, 21.0, 215.0, 266.0, 1761048513, 36537518964406914
zero, 1999361, 1999361, 0, 31466, 13.0, 17.0, 22.0, 220.0, 270.0, 1761048534, 36537568837223748
zero, 2124773, 2124773, 0, 34776, 14.0, 17.0, 26.0, 248.0, 356.0, 1761048555, 36537619610962908
zero, 2249174, 2249174, 0, 35950, 14.0, 18.0, 25.0, 256.0, 346.0, 1761048576, 36537670843252674
zero, 2371763, 2371763, 0, 38281, 14.0, 19.0, 27.0, 232.0, 379.0, 1761048598, 36537724081650111
zero, 2496912, 2496912, 0, 40783, 15.0, 21.0, 44.0, 261.0, 417.0, 1761048621, 36537776876794278
"""

log_data_tangle = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 129606, 129606, 0, 1721, 14.0, 17.0, 19.0, 116.0, 209.0, 1761045752, 36530909127421260
zero, 254076, 254076, 0, 3499, 14.0, 18.0, 21.0, 134.0, 212.0, 1761045770, 36530951309101528
zero, 378595, 378595, 0, 5261, 13.0, 18.0, 20.0, 147.0, 221.0, 1761045788, 36530993750933424
zero, 503273, 503273, 0, 7037, 12.0, 18.0, 21.0, 157.0, 227.0, 1761045805, 36531036457318940
zero, 627788, 627788, 0, 8635, 11.0, 16.0, 20.0, 152.0, 233.0, 1761045823, 36531079413920745
zero, 752278, 752278, 0, 10578, 11.0, 16.0, 21.0, 158.0, 229.0, 1761045841, 36531122734042416
zero, 877088, 877088, 0, 12699, 11.0, 17.0, 22.0, 167.0, 234.0, 1761045860, 36531166742711560
zero, 1001484, 1001484, 0, 14471, 11.0, 16.0, 22.0, 171.0, 235.0, 1761045878, 36531211111227462
zero, 1127397, 1127397, 0, 16765, 11.0, 15.0, 22.0, 181.0, 247.0, 1761045897, 36531256424024541
zero, 1251283, 1251283, 0, 18237, 11.0, 15.0, 21.0, 187.0, 249.0, 1761045917, 36531302554726038
zero, 1375874, 1375874, 0, 20535, 12.0, 15.0, 19.0, 199.0, 255.0, 1761045936, 36531349070270631
zero, 1501093, 1501093, 0, 22128, 12.0, 15.0, 20.0, 209.0, 261.0, 1761045956, 36531396247339920
zero, 1624878, 1624878, 0, 24500, 12.0, 15.0, 20.0, 202.0, 263.0, 1761045976, 36531444493003389
zero, 1751480, 1751480, 0, 26450, 12.0, 16.0, 20.0, 211.0, 271.0, 1761045996, 36531493291495044
zero, 1875256, 1875256, 0, 29105, 13.0, 16.0, 21.0, 212.0, 267.0, 1761046017, 36531542277199164
zero, 1999076, 1999076, 0, 32124, 13.0, 17.0, 22.0, 222.0, 271.0, 1761046037, 36531592119048834
zero, 2123854, 2123854, 0, 35006, 14.0, 18.0, 32.0, 240.0, 326.0, 1761046059, 36531642501831795
zero, 2249552, 2249552, 0, 35711, 14.0, 18.0, 25.0, 262.0, 348.0, 1761046080, 36531693700787715
zero, 2371367, 2371367, 0, 40311, 15.0, 19.0, 28.0, 230.0, 381.0, 1761046102, 36531745587180882
zero, 2496508, 2496508, 0, 44641, 16.0, 22.0, 80.0, 266.0, 416.0, 1761046124, 36531798192133632
"""

# Read the log data into a pandas DataFrame.
# skipinitialspace=True helps to trim extra spaces after commas.
df = pd.read_csv(StringIO(log_data), skipinitialspace=True)
df_tangle = pd.read_csv(StringIO(log_data_tangle), skipinitialspace=True)

# Clean up the header names by stripping any extra whitespace.
df.columns = [col.strip() for col in df.columns]

# Convert relevant columns from strings to numeric types.
df['Target'] = pd.to_numeric(df['Target'], errors='coerce')
df['99.9th'] = pd.to_numeric(df['99.9th'], errors='coerce')
df['99.99th'] = pd.to_numeric(df['99.99th'], errors='coerce')
df_tangle['99.9th'] = pd.to_numeric(df_tangle['99.9th'], errors='coerce')
df_tangle['99.99th'] = pd.to_numeric(df_tangle['99.99th'], errors='coerce')

# Set up the figure
plt.figure(figsize=(11, 8))

# Plot the percentiles versus the number of packets processed (Target)
# ====== p99.99th percentile here ======
plt.plot(df['Target'], df['99.99th'], color='orange', marker='s', linestyle='-', label='Tangle without prefetching')
plt.plot(df_tangle['Target'], df_tangle['99.99th'], color='blue', marker='o', linestyle='--', label='Tangle with prefetching')
# ====== p99.9th percentile here ======
# plt.plot(df['Target'], df['99.9th'], color='orange', marker='^', linestyle='-', label='Caladan')
# plt.plot(df_tangle['Target'], df_tangle['99.9th'], color='green', marker='o', linestyle='-', label='Tangle')

# Labeling the plot
plt.xlabel("Number of Packets (millions)")
plt.ylabel("Latency (μs)")
plt.title("")
plt.legend()
plt.grid(True)

# Disable scientific notation on the x-axis to remove the "1e6" offset notation.
# plt.ticklabel_format(style="sci", axis="x")

# Save the plot to a file
plt.savefig("prefetch_latency_comparison.pdf")

# caladan: 25251508 hashtable reads, 3931051452 cycles, 1.61 seconds
# tangle:  1 hashtable read = 3231 cycles, 1.35 µs
# hz 2400000000
plt.show()