import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import math
import random

# -----------------------------
# Input data (keep SAME names)
# -----------------------------
caladan_log_data = """
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
zero, 1250789, 1250789, 0, 6215828, 12.0, 15.0, 27.0, 359.0, 285.0, 1744810481, 4518430060809333
zero, 1367417, 1367417, 0, 7261295, 12.0, 15.0, 24.0, 309.0, 380.0, 1744810510, 4518497950144125
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

# -----------------------------
# Styling (match your thesis plots)
# -----------------------------
plt.rcParams['font.size'] = 22
plt.rcParams['axes.titlesize'] = 24
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['xtick.labelsize'] = 22
plt.rcParams['ytick.labelsize'] = 22

# -----------------------------
# Helpers
# -----------------------------
def parse_latency_log(log_text: str) -> pd.DataFrame:
    df = pd.read_csv(StringIO(log_text.strip()), skipinitialspace=True)
    df.columns = [c.strip() for c in df.columns]

    numeric_cols = ["90th", "99th", "99.9th", "99.99th"]
    missing = [c for c in numeric_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}. Parsed columns: {df.columns.tolist()}")

    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["Target", "Median", "99th", "99.99th"])
    df["packets_millions"] = df["Target"] / 1_000_000.0
    return df


def synth_samples_from_percentiles(median: float, p99: float, p9999: float, n: int = 1200) -> list:
    median = max(float(median), 1e-9)
    p99 = max(float(p99), median * 1.000001)

    z99 = 2.3263478740408408
    mu = math.log(median)
    sigma = (math.log(p99) - mu) / z99
    sigma = max(sigma, 1e-6)

    cap = float(p9999) if float(p9999) > 0 else p99

    samples = []
    for _ in range(n):
        x = random.lognormvariate(mu, sigma)
        if x > cap:
            x = cap - (cap * 0.02 * random.random())
        samples.append(x)
    return samples


# -----------------------------
# Build dataframes
# -----------------------------
df_caladan = parse_latency_log(caladan_log_data)
df_tangle = parse_latency_log(log_data_tangle)

min_len = min(len(df_caladan), len(df_tangle))
df_caladan = df_caladan.iloc[:min_len].reset_index(drop=True)
df_tangle = df_tangle.iloc[:min_len].reset_index(drop=True)

# ----------------------------------------------------------
# Reduce number of boxplots only after 1.7 million packets/s
# ----------------------------------------------------------
THRESHOLD_MILLIONS = 1.7

mask_head = df_caladan["packets_millions"] <= THRESHOLD_MILLIONS
mask_tail = ~mask_head

df_head_caladan = df_caladan.loc[mask_head]
df_tail_caladan = df_caladan.loc[mask_tail]

df_head_tangle = df_tangle.loc[mask_head]
df_tail_tangle = df_tangle.loc[mask_tail]

# Keep all head points; downsample only the tail
tail_step = 2  # increase to 3 if still too dense
df_tail_caladan = df_tail_caladan.iloc[::tail_step]
df_tail_tangle = df_tail_tangle.iloc[::tail_step]

df_caladan = pd.concat([df_head_caladan, df_tail_caladan], ignore_index=True)
df_tangle = pd.concat([df_head_tangle, df_tail_tangle], ignore_index=True)

# Y positions now (Number of Packets in millions)  <-- CHANGED (was X positions)
y = df_caladan["packets_millions"].tolist()

# Side-by-side offset on Y (in "millions of packets" units)  <-- CHANGED (was X offset)
delta = 0.03
y_caladan = [v - delta for v in y]
y_tangle = [v + delta for v in y]

caladan_samples = [
    synth_samples_from_percentiles(row["Median"], row["99th"], row["99.99th"])
    for _, row in df_caladan.iterrows()
]
tangle_samples = [
    synth_samples_from_percentiles(row["Median"], row["99th"], row["99.99th"])
    for _, row in df_tangle.iterrows()
]

# -----------------------------
# Plot (horizontal boxplots now)  <-- CHANGED
# -----------------------------
fig, ax = plt.subplots(figsize=(14, 8))

bp_caladan = ax.boxplot(
    caladan_samples,
    positions=y_caladan,   # <-- CHANGED
    widths=0.05,           # width measured in "y-axis units" (millions)  <-- CHANGED comment
    patch_artist=True,
    showfliers=False,
    whis=(5, 99),
    vert=False,            # <-- CHANGED
)

bp_tangle = ax.boxplot(
    tangle_samples,
    positions=y_tangle,    # <-- CHANGED
    widths=0.05,
    patch_artist=True,
    showfliers=False,
    whis=(5, 99),
    vert=False,            # <-- CHANGED
)

# Colors
for b in bp_caladan["boxes"]:
    b.set_facecolor("#9ecae1")
    b.set_edgecolor("black")
    b.set_linewidth(1.0)

for b in bp_tangle["boxes"]:
    b.set_facecolor("#e41a1c")
    b.set_edgecolor("black")
    b.set_linewidth(1.0)

def style_bp(bp):
    for key in ["whiskers", "caps", "medians"]:
        for line in bp[key]:
            line.set_color("black")
            line.set_linewidth(1.0)

style_bp(bp_caladan)
style_bp(bp_tangle)

# Axis labels swapped  <-- CHANGED
ax.set_xlabel("Latency (microseconds)")
ax.set_ylabel("Number of Packets (millions)")

ax.grid(True, which="major", axis="both", linestyle="--", linewidth=0.6, alpha=0.6)

# Y ticks: show fewer to keep it readable  <-- CHANGED (was X ticks)
num_ticks = 6
step = max(1, len(y) // num_ticks)
yticks = y[::step]
ax.set_yticks(yticks)
ax.set_yticklabels([f"{v:.2f}" for v in yticks], rotation=0)

# zoom in on the most relevant range (e.g., up to 100 microseconds)
ax.set_xlim(left=0, right=100)

# packets range now on Y axis  <-- CHANGED
ax.set_ylim(bottom=min(y) - 0.10, top=max(y) + 0.10)

# Legend (top-right)
caladan_proxy = plt.Line2D([0], [0], color="#9ecae1", lw=10)
tangle_proxy = plt.Line2D([0], [0], color="#e41a1c", lw=10)
ax.legend(
    [caladan_proxy, tangle_proxy],
    ["Caladan", "Tangle"],
    loc="upper right",
    frameon=True
)

plt.tight_layout()
plt.savefig("tangle_vs_caladan_latency_boxplot.pdf", bbox_inches="tight")
plt.show()
