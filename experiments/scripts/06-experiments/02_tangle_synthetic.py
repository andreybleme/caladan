import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

# Log data as a multiline string
log_data_tangle = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 603955, 603955, 0, 11292, 12.0, 15.0, 21.0, 142.0, 210.0, 1744648076, 4129725750941037
zero, 803477, 803477, 0, 11781, 13.0, 19.0, 23.0, 184.0, 241.0, 1744648095, 4129772105164400
zero, 1001175, 1001175, 0, 15317, 11.0, 15.0, 19.0, 169.0, 240.0, 1744648115, 4129819866984288
zero, 1249629, 1249629, 0, 88073, 12.0, 16.0, 21.0, 192.0, 255.0, 1744648199, 4130022062983059
zero, 1600565, 1600565, 0, 263882, 12.0, 16.0, 23.0, 261.0, 301.0, 1744648245, 4130132155126428
zero, 1817890, 1817890, 0, 2578351, 13.0, 17.0, 60.0, 255.0, 285.0, 1744648342, 4130363020310367
zero, 1973209, 1973209, 0, 2677768, 13.0, 17.0, 55.0, 309.0, 369.0, 1744648367, 4130424416054292
zero, 2089455, 2089455, 0, 4661205, 13.0, 16.0, 62.0, 338.0, 427.0, 1744648420, 4130550104105223
zero, 2099455, 2099455, 0, 6215828, 12.0, 15.0, 67.0, 354.0, 436.0, 1744810481, 4518430060809333
"""

# Read the log data into a pandas DataFrame.
# skipinitialspace=True helps to trim extra spaces after commas.
df_tangle = pd.read_csv(StringIO(log_data_tangle), skipinitialspace=True)

# Clean up the header names by stripping any extra whitespace.
df_tangle.columns = [col.strip() for col in df_tangle.columns]

# Convert relevant columns from strings to numeric types.
df_tangle['Target'] = pd.to_numeric(df_tangle['Target'], errors='coerce')
df_tangle['Median'] = pd.to_numeric(df_tangle['Median'], errors='coerce')
df_tangle['90th'] = pd.to_numeric(df_tangle['90th'], errors='coerce')
df_tangle['99th'] = pd.to_numeric(df_tangle['99th'], errors='coerce')
df_tangle['99.9th'] = pd.to_numeric(df_tangle['99.9th'], errors='coerce')
df_tangle['99.99th'] = pd.to_numeric(df_tangle['99.99th'], errors='coerce')
df_tangle['99.9th'] = pd.to_numeric(df_tangle['99.9th'], errors='coerce')
df_tangle['99.99th'] = pd.to_numeric(df_tangle['99.99th'], errors='coerce')

# Set up the figure
plt.figure(figsize=(10, 6))

# Plot the percentiles versus the number of packets processed (Target)
# ====== p99.99th percentile here ======
plt.plot(df_tangle['Target'], df_tangle['Median'], color='black', marker='*', linestyle='-', label='Median')
plt.plot(df_tangle['Target'], df_tangle['90th'], color='#baba3f', marker='x', linestyle='-', label='90th Percentile')
plt.plot(df_tangle['Target'], df_tangle['99th'], color='#d16a41', marker='D', linestyle='-', label='99th Percentile')
plt.plot(df_tangle['Target'], df_tangle['99.9th'], color='green', marker='^', linestyle='-', label='99.9th Percentile')
plt.plot(df_tangle['Target'], df_tangle['99.99th'], color='blue', marker='o', linestyle='-', label='99.99th Percentile')
# ====== p99.9th percentile here ======
#plt.plot(df['Target'], df['99.9th'], color='orange', marker='^', linestyle='-', label='Caladan 99.9th Percentile')
#plt.plot(df_tangle['Target'], df_tangle['99.9th'], color='green', marker='o', linestyle='-', label='Tangle 99.9th Percentile')

# Labeling the plot
plt.xlabel("Number of Packets (millions)")
plt.ylabel("Latency (μs)")
plt.title("")
plt.legend()
plt.grid(True)

# Disable scientific notation on the x-axis to remove the "1e6" offset notation.
# plt.ticklabel_format(style="sci", axis="x")

# Save the plot to a file
plt.savefig("latency_tangle.pdf")

# caladan: 25251508 hashtable reads, 3931051452 cycles, 1.61 seconds
# tangle:  1 hashtable read = 3231 cycles, 1.35 µs
# hz 2400000000
