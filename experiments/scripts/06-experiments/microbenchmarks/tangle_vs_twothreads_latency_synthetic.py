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
zero, 129567, 129567, 0, 7201, 12.0, 18.0, 22.0, 165.0, 228.0, 1744810262, 4517905260852237
zero, 264131, 264131, 0, 9251, 11.0, 15.0, 21.0, 170.0, 237.0, 1744810283, 4517955449645319
zero, 372835, 372835, 0, 11852, 12.0, 16.0, 23.0, 185.0, 249.0, 1744810305, 4518007910689680
zero, 501572, 501572, 0, 14078, 12.0, 15.0, 21.0, 201.0, 252.0, 1744810328, 4518062754739965
zero, 621859, 621859, 0, 17147, 12.0, 15.0, 20.0, 228.0, 260.0, 1744810351, 4518119369184468
zero, 752338, 752338, 0, 20058, 12.0, 15.0, 22.0, 234.0, 270.0, 1744810376, 4518178029876939
zero, 897362, 897362, 0, 79767, 13.0, 16.0, 38.0, 229.0, 244.0, 1744810401, 4518238880193495
zero, 1011474, 1011474, 0, 1036711, 13.0, 15.0, 71.0, 249.0, 267.0, 1744810427, 4518300323709195
zero, 1225116, 1225116, 0, 3168678, 13.0, 15.0, 40.0, 255.0, 285.0, 1744810454, 4518363926345751
zero, 1350989, 1350989, 0, 6215828, 12.0, 15.0, 27.0, 359.0, 271.0, 1744810481, 4518430060809333
zero, 1367817, 1367817, 0, 7261295, 12.0, 15.0, 24.0, 300.0, 319.0, 1744810510, 4518497950144125
zero, 1435120, 1435120, 0, 10478303, 12.0, 15.0, 25.0, 301.0, 351.0, 1744810539, 4518567627061170
zero, 1498251, 1498251, 0, 12371483, 12.0, 15.0, 28.0, 321.0, 349.0, 1744810570, 4518641465034459
zero, 1633612, 1633612, 0, 13152188, 12.0, 14.0, 21.0, 241.0, 262.0, 1744810600, 4518713789232357
zero, 1779053, 1779053, 0, 15322467, 12.0, 14.0, 24.0, 249.0, 279.0, 1744810632, 4518791716504689
zero, 1803118, 1803118, 0, 17166512, 12.0, 14.0, 21.0, 237.0, 261.0, 1744810665, 4518870332741106
zero, 1831268, 1831268, 0, 19309612, 12.0, 14.0, 21.0, 249.0, 279.0, 1744810699, 4518951258380769
zero, 1887201, 1887201, 0, 22348730, 12.0, 14.0, 20.0, 268.0, 429.0, 1744810733, 4519032088527924
zero, 1991349, 1991349, 0, 23548424, 12.0, 14.0, 21.0, 303.0, 512.0, 1744810767, 4519114951642887
zero, 2103854, 2103854, 0, 26450091, 12.0, 15.0, 27.0, 321.0, 572.0, 1744810803, 4519200873455925
"""

log_data_tangle = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 129606, 129606, 0, 1721, 14.0, 17.0, 19.0, 116.0, 209.0, 1761045752, 36530909127421260
zero, 254076, 254076, 0, 3499, 14.0, 18.0, 21.0, 134.0, 216.0, 1761045770, 36530951309101528
zero, 378595, 378595, 0, 5261, 13.0, 18.0, 20.0, 147.0, 227.0, 1761045788, 36530993750933424
zero, 503273, 503273, 0, 7037, 12.0, 18.0, 21.0, 157.0, 235.0, 1761045805, 36531036457318940
zero, 627788, 627788, 0, 8635, 11.0, 16.0, 20.0, 152.0, 229.0, 1761045823, 36531079413920745
zero, 752278, 752278, 0, 10578, 11.0, 16.0, 21.0, 158.0, 233.0, 1761045841, 36531122734042416
zero, 877088, 877088, 0, 12699, 11.0, 17.0, 22.0, 167.0, 236.0, 1761045860, 36531166742711560
zero, 1001484, 1001484, 0, 14471, 11.0, 16.0, 22.0, 171.0, 239.0, 1761045878, 36531211111227462
zero, 1127397, 1127397, 0, 16765, 11.0, 15.0, 22.0, 181.0, 247.0, 1761045897, 36531256424024541
zero, 1251283, 1251283, 0, 18237, 11.0, 15.0, 21.0, 187.0, 249.0, 1761045917, 36531302554726038
zero, 1375874, 1375874, 0, 20535, 12.0, 15.0, 19.0, 199.0, 255.0, 1761045936, 36531349070270631
zero, 1501093, 1501093, 0, 22128, 12.0, 15.0, 20.0, 209.0, 261.0, 1761045956, 36531396247339920
zero, 1624878, 1624878, 0, 24500, 12.0, 15.0, 20.0, 202.0, 263.0, 1761045976, 36531444493003389
zero, 1751480, 1751480, 0, 26450, 12.0, 16.0, 20.0, 211.0, 271.0, 1761045996, 36531493291495044
zero, 1875256, 1875256, 0, 29105, 13.0, 16.0, 21.0, 212.0, 267.0, 1761046017, 36531542277199164
zero, 1999076, 1999076, 0, 32124, 13.0, 17.0, 22.0, 222.0, 271.0, 1761046037, 36531592119048834
zero, 2123854, 2123854, 0, 35006, 14.0, 18.0, 32.0, 240.0, 326.0, 1761046059, 36531642501831795
zero, 2249552, 2249552, 0, 35711, 14.0, 18.0, 25.0, 262.0, 351.0, 1761046080, 36531693700787715
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
plt.plot(df['Target'], df['99.99th'], color='purple', marker='s', linestyle='-', label='Tangle single-core')
plt.plot(df_tangle['Target'], df_tangle['99.99th'], color='blue', marker='o', linestyle='-', label='Tangle')
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
plt.savefig("tangle_vs_twothreads_latency.pdf")

# caladan: 25251508 hashtable reads, 3931051452 cycles, 1.61 seconds
# tangle:  1 hashtable read = 3231 cycles, 1.35 µs
# hz 2400000000
plt.show()