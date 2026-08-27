import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# ===== Motivation section logs =====
# Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
# zero, 603955, 603955, 0, 8564, 11.0, 14.0, 18.0, 140.0, 215.0, 1744662961, 4165366635171680
# zero, 803477, 803477, 0, 13376, 11.0, 15.0, 21.0, 165.0, 228.0, 1744662980, 4165413115613988
# zero, 1001175, 1001175, 0, 18569, 12.0, 16.0, 22.0, 193.0, 247.0, 1744643479, 4118719974371202
# zero, 1249629, 1249629, 0, 30023, 12.0, 15.0, 22.0, 197.0, 264.0, 1744643522, 41188217983181910
# zero, 1600565, 1600565, 0, 269683, 12.0, 16.0, 22.0, 260.0, 305.0, 1744643589, 4118982089638377
# zero, 1817890, 1817890, 0, 2535977, 13.0, 16.0, 34.0, 306.0, 356.0, 1744643712, 4119276848413887
# zero, 1973209, 1973209, 0, 5036621, 13.0, 16.0, 40.0, 352.0, 429.0, 1744643737, 4119337629426504
# zero, 2089455, 1989455, 0, 4625960, 12.0, 16.0, 31.0, 349.0, 435.0, 1744643764, 4119401128731042
# zero, 2099455, 1812936, 0, 6215828, 12.0, 15.0, 27.0, 359.0, 629.0, 1744810481, 4518430060809333

# Log data as a multiline string
log_data = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 129567, 129567, 0, 7201, 12.0, 18.0, 22.0, 169.0, 238.0, 1744810262, 4517905260852237
zero, 254181, 254181, 0, 9251, 11.0, 15.0, 21.0, 170.0, 237.0, 1744810283, 4517955449645319
zero, 378845, 378845, 0, 11852, 12.0, 16.0, 23.0, 195.0, 259.0, 1744810305, 4518007910689680
zero, 503472, 503472, 0, 14078, 12.0, 15.0, 21.0, 208.0, 265.0, 1744810328, 4518062754739965
zero, 627959, 627959, 0, 17147, 12.0, 15.0, 20.0, 228.0, 260.0, 1744810351, 4518119369184468
zero, 752338, 752338, 0, 20058, 12.0, 15.0, 22.0, 234.0, 270.0, 1744810376, 4518178029876939
zero, 877382, 877382, 0, 79767, 13.0, 16.0, 38.0, 239.0, 264.0, 1744810401, 4518238880193495
zero, 1001474, 1001474, 0, 1036711, 13.0, 15.0, 71.0, 259.0, 287.0, 1744810427, 4518300323709195
zero, 1125116, 1125116, 0, 3168678, 13.0, 15.0, 40.0, 255.0, 285.0, 1744810454, 4518363926345751
zero, 1250789, 1250789, 0, 6215828, 12.0, 15.0, 27.0, 346.0, 379.0, 1744810481, 4518430060809333
zero, 1367417, 1367417, 0, 7261295, 12.0, 15.0, 24.0, 319.0, 380.0, 1744810510, 4518497950144125
zero, 1497120, 1497120, 0, 10478303, 12.0, 15.0, 25.0, 302.0, 356.0, 1744810539, 4518567627061170
zero, 1598351, 1598351, 0, 12371483, 12.0, 15.0, 28.0, 336.0, 397.0, 1744810570, 4518641465034459
zero, 1733612, 1733612, 0, 13152188, 12.0, 14.0, 21.0, 241.0, 262.0, 1744810600, 4518713789232357
zero, 1779053, 1779053, 0, 15322467, 12.0, 14.0, 24.0, 249.0, 279.0, 1744810632, 4518791716504689
zero, 1803118, 1803118, 0, 17166512, 12.0, 14.0, 21.0, 237.0, 261.0, 1744810665, 4518870332741106
zero, 1822368, 1822368, 0, 19309612, 12.0, 14.0, 21.0, 249.0, 279.0, 1744810699, 4518951258380769
zero, 1847202, 1847202, 0, 22348730, 12.0, 14.0, 20.0, 268.0, 429.0, 1744810733, 4519032088527924
zero, 1904369, 1904369, 0, 23548424, 12.0, 14.0, 21.0, 300.0, 535.0, 1744810767, 4519114951642887
zero, 1964553, 1964553, 0, 26450091, 12.0, 15.0, 27.0, 359.0, 629.0, 1744810803, 4519200873455925
"""

# Read the log data into a pandas DataFrame.
# skipinitialspace=True helps to trim extra spaces after commas.
df = pd.read_csv(StringIO(log_data), skipinitialspace=True)

# Clean up the header names by stripping any extra whitespace.
df.columns = [col.strip() for col in df.columns]

# Convert relevant columns from strings to numeric types.
df['Target'] = pd.to_numeric(df['Target'], errors='coerce')
df['99.9th'] = pd.to_numeric(df['99.9th'], errors='coerce')
df['99.99th'] = pd.to_numeric(df['99.99th'], errors='coerce')

# Set up the figure
plt.figure(figsize=(10, 6))

# Plot the percentiles versus the number of packets processed (Target)
plt.plot(df['Target'], df['99.9th'], color='orange', marker='s', linestyle='--', label='99.9th Percentile')
plt.plot(df['Target'], df['99.99th'], color='red', marker='^', linestyle='-', label='99.99th Percentile')

# Labeling the plot
plt.xlabel("Number of Packets (millions)", fontsize=16)
plt.ylabel("Latency (μs)", fontsize=16)
plt.title("")
plt.legend(fontsize=16)
plt.grid(True)

# Disable scientific notation on the x-axis to remove the "1e6" offset notation.
# plt.ticklabel_format(style="sci", axis="x")

plt.rcParams.update({'font.size': 16})
# Save the plot to a file
plt.savefig("motivation_caladan_latency_synthetic.pdf")
plt.show()

# caladan: 25251508 hashtable reads, 3931051452 cycles, 1.61 seconds
# tangle:  1 hashtable read = 3231 cycles, 1.35 µs
# hz 2400000000
