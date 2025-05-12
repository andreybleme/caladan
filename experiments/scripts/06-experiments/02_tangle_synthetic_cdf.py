import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14


# === log data (unchanged) ===
log_data = """
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

# === load into DataFrame ===
df = pd.read_csv(StringIO(log_data), skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]

# convert to numeric
for col in ['Median', '90th', '99th', '99.9th', '99.99th']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# === compute & plot empirical CDFs ===
plt.figure(figsize=(10, 6))
percentiles = ['Median', '90th', '99th', '99.9th', '99.99th']
colors     = ['black', '#baba3f', '#d16a41', 'green',    'blue']
markers    = ['*', 'x', 'D', '^', 'o']

plt.figure(figsize=(10,6))
for pct, col, m in zip(percentiles, colors, markers):
    vals = df[pct].dropna().values
    vals_sorted = np.sort(vals)
    cdf = np.arange(1, len(vals_sorted)+1) / len(vals_sorted)
    # draw the steps + markers
    plt.step(vals_sorted, cdf, where='post',
             color=col, linewidth=2,
             marker=m, markersize=6,
             label=f'{pct} Percentile')

plt.xlabel("Latency (μs)", fontsize=14)
plt.ylabel("CDF", fontsize=14)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("latency_tangle_cdf.pdf")
plt.show()
