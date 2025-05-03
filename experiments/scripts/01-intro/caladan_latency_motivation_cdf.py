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

# === load into DataFrame ===
df = pd.read_csv(StringIO(log_data), skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]

# convert to numeric
for col in ['99.9th', '99.99th']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# === compute & plot empirical CDFs ===
plt.figure(figsize=(10, 6))
percentiles = ['99.9th', '99.99th']
colors     = ['orange',    'red']
markers    = ['s', '^']

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
plt.savefig("motivation_caladan_latency_cdf.pdf")
plt.show()
