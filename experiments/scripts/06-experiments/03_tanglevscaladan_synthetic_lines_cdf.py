import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24

# === log data for Caladan ===
log_data_caladan = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 603955, 603955, 0, 8564, 11.0, 14.0, 18.0, 140.0, 215.0, 1744662961, 4165366635171680
zero, 803477, 803477, 0, 13376, 11.0, 15.0, 21.0, 165.0, 228.0, 1744662980, 4165413115613988
zero, 1001175, 1001175, 0, 18569, 12.0, 16.0, 22.0, 193.0, 247.0, 1744643479, 4118719974371202
zero, 1249629, 1249629, 0, 30023, 12.0, 15.0, 22.0, 197.0, 264.0, 1744643522, 41188217983181910
zero, 1600565, 1600565, 0, 269683, 12.0, 16.0, 22.0, 260.0, 305.0, 1744643589, 4118982089638377
zero, 1817890, 1817890, 0, 2535977, 13.0, 16.0, 34.0, 306.0, 356.0, 1744643712, 4119276848413887
zero, 1973209, 1973209, 0, 5036621, 13.0, 16.0, 40.0, 352.0, 429.0, 1744643737, 4119337629426504
zero, 2089455, 1989455, 0, 4625960, 12.0, 16.0, 31.0, 356.0, 535.0, 1744643764, 4119401128731042
zero, 2099455, 1812936, 0, 6215828, 12.0, 15.0, 27.0, 390.0, 629.0, 1744810481, 4518430060809333
"""

# === log data for Tangle ===
log_data_tangle = """
Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
zero, 603955, 603955, 0, 11292, 12.0, 15.0, 21.0, 142.0, 210.0, 1744648076, 4129725750941037
zero, 803477, 803477, 0, 11781, 13.0, 19.0, 23.0, 184.0, 241.0, 1744648095, 4129772105164400
zero, 1001175, 1001175, 0, 15317, 11.0, 15.0, 19.0, 169.0, 240.0, 1744648115, 4129819866984288
zero, 1249629, 1249629, 0, 88073, 12.0, 16.0, 21.0, 192.0, 255.0, 1744648199, 4130022062983059
zero, 1600565, 1600565, 0, 263882, 12.0, 16.0, 23.0, 261.0, 301.0, 1744648245, 4130132155126428
zero, 1817890, 1817890, 0, 2578351, 13.0, 17.0, 60.0, 255.0, 285.0, 1744648342, 4130363020310367
zero, 1973209, 1973209, 0, 2677768, 13.0, 17.0, 55.0, 309.0, 369.0, 1744648367, 4130424416054292
zero, 2089455, 2089455, 0, 4661205, 13.0, 16.0, 67.0, 338.0, 427.0, 1744648420, 4130550104105223
zero, 2099455, 2099455, 0, 6215828, 12.0, 15.0, 27.0, 354.0, 436.0, 1744810481, 4518430060809333
"""

# load into DataFrames
df_cal = pd.read_csv(StringIO(log_data_caladan), skipinitialspace=True)
df_tan = pd.read_csv(StringIO(log_data_tangle), skipinitialspace=True)
for df in (df_cal, df_tan):
    df.columns = [c.strip() for c in df.columns]
    df['99.9th'] = pd.to_numeric(df['99.9th'], errors='coerce')

# compute & plot empirical CDFs for 99.9th only
plt.figure(figsize=(11, 8))

# p99.99 here
for df, color, marker, label in [
    (df_cal,  'red',     '^', 'Caladan 99.99th percentile'),
    (df_tan,  'blue',    'o', 'Tangle 99.99.th percentile')    
]:
# p99.9 here
# for df, color, marker, label in [
#     (df_cal,  'orange',     '^', 'Caladan 99.9th percentile'),
#     (df_tan,  'green',    'o', 'Tangle 99.9.th percentile')    
# ]:
    vals = df['99.9th'].dropna().values
    vals_sorted = np.sort(vals)
    cdf = np.arange(1, len(vals_sorted)+1) / len(vals_sorted)
    plt.step(vals_sorted, cdf, where='post',
             color=color, linewidth=2,
             marker=marker, markersize=6,
             label=label)

plt.xlabel("Latency (μs)", fontsize=24)
plt.ylabel("CDF", fontsize=24)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_caladanvstangle_99d99_cdf.pdf")
plt.show()
