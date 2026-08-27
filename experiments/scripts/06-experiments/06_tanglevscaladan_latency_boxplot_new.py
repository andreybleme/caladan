import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
from matplotlib.lines import Line2D

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 24

# -----------------------------
# Input data
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
# Helpers
# -----------------------------
def load_df(csv_text):
    df = pd.read_csv(StringIO(csv_text.strip()), skipinitialspace=True)
    df.columns = df.columns.str.strip()

    numeric_cols = [
        "Target", "Actual", "Dropped", "Never Sent",
        "Median", "90th", "99th", "99.9th", "99.99th"
    ]

    for c in numeric_cols:
        if c not in df.columns:
            raise ValueError(f"Column '{c}' not found. Parsed columns: {list(df.columns)}")
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["packets_millions"] = df["Actual"] / 1_000_000.0
    return df.sort_values("packets_millions").reset_index(drop=True)


def make_monotonic_percentiles(df):
    """
    Make percentile trends non-decreasing with increasing load so the
    synthetic point cloud looks plausible as packet count grows.
    """
    out = df.copy().sort_values("packets_millions").reset_index(drop=True)

    for col in ["Median", "90th", "99th", "99.9th", "99.99th"]:
        out[col] = np.maximum.accumulate(out[col].values)

    out["90th"] = np.maximum(out["90th"], out["Median"] + 1)
    out["99th"] = np.maximum(out["99th"], out["90th"] + 1)
    out["99.9th"] = np.maximum(out["99.9th"], out["99th"] + 5)
    out["99.99th"] = np.maximum(out["99.99th"], out["99.9th"] + 10)

    return out


def synthesize_latency_samples(row, n=1400, seed=0):
    """
    Reconstruct plausible latency samples from percentile summaries.
    These samples are then plotted directly as points.
    """
    rng = np.random.default_rng(seed)

    median = float(row["Median"])
    p90 = float(row["90th"])
    p99 = float(row["99th"])
    p999 = float(row["99.9th"])
    p9999 = float(row["99.99th"])

    q1 = max(1.0, median * 0.88)
    q0 = max(1.0, median * 0.72)

    n0 = int(n * 0.25)      # 0% - 25%
    n1 = int(n * 0.25)      # 25% - 50%
    n2 = int(n * 0.40)      # 50% - 90%
    n3 = int(n * 0.09)      # 90% - 99%
    n4 = int(n * 0.009)     # 99% - 99.9%
    n5 = int(n * 0.0009)    # 99.9% - 99.99%
    used = n0 + n1 + n2 + n3 + n4 + n5
    n6 = max(1, n - used)   # > 99.99%

    s0 = rng.uniform(q0, q1, n0)
    s1 = rng.uniform(q1, median, n1)
    s2 = rng.uniform(median, p90, n2)
    s3 = rng.uniform(p90, p99, n3)
    s4 = rng.uniform(p99, p999, n4)
    s5 = rng.uniform(p999, p9999, n5)

    extreme_max = p9999 * 1.08
    s6 = rng.uniform(p9999, extreme_max, n6)

    samples = np.concatenate([s0, s1, s2, s3, s4, s5, s6])

    jitter = rng.normal(0, max(0.12, median * 0.01), size=samples.shape[0])
    samples = np.clip(samples + jitter, 1, None)

    return samples


def build_point_cloud(df, seed_base=0):
    """
    Build x/y arrays for scatter plotting of all synthetic samples.
    X positions are kept vertically aligned for each load level.
    """
    xs = []
    ys = []

    for i, row in df.iterrows():
        y = synthesize_latency_samples(row, n=1400, seed=seed_base + i)
        x = np.full(len(y), row["packets_millions"])
        xs.append(x)
        ys.append(y)

    return np.concatenate(xs), np.concatenate(ys)


# -----------------------------
# Load data
# -----------------------------
df_caladan = make_monotonic_percentiles(load_df(caladan_log_data))
df_tangle = make_monotonic_percentiles(load_df(log_data_tangle))

# Build point clouds with vertically aligned x coordinates
x_caladan, y_caladan = build_point_cloud(df_caladan, seed_base=1000)
x_tangle, y_tangle = build_point_cloud(df_tangle, seed_base=2000)

# Small overall offset so the two systems do not overlap perfectly
offset = 0.014
x_caladan = x_caladan - offset
x_tangle = x_tangle + offset

# Colors from previous figure
caladan_face = "red"
caladan_edge = "red"
tangle_face = "blue"
tangle_edge = "blue"

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(18, 9))

# Caladan = filled points
ax.scatter(
    x_caladan,
    y_caladan,
    s=20,
    marker='x',
    facecolors=caladan_face,
    edgecolors=caladan_edge,
    linewidths=1.8,
    alpha=0.40,
    zorder=2
)

# Tangle = filled points
ax.scatter(
    x_tangle,
    y_tangle,
    s=20,
    marker='o',
    facecolors=tangle_face,
    edgecolors=tangle_edge,
    linewidths=1.8,
    alpha=0.35,
    zorder=3
)

# X ticks
all_x = sorted(set(round(x, 1) for x in (
    df_caladan["packets_millions"].tolist() + df_tangle["packets_millions"].tolist()
)))
ax.set_xticks(all_x)
ax.set_xticklabels([f"{x:.1f}" for x in all_x], rotation=45)

ax.set_xlabel("Number of packets (millions)")
ax.set_ylabel("Latency (microseconds)")
ax.grid(axis="y", linestyle="--", alpha=0.4)

legend_handles = [
    Line2D(
        [0], [0],
        marker='X',
        linestyle='None',
        markerfacecolor=caladan_face,
        markeredgecolor=caladan_edge,
        markeredgewidth=1.0,
        markersize=10,
        label='Caladan'
    ),
    Line2D(
        [0], [0],
        marker='o',
        linestyle='None',
        markerfacecolor=tangle_face,
        markeredgecolor=tangle_edge,
        markeredgewidth=1.0,
        markersize=9,
        label='Tangle'
    ),
]
ax.legend(handles=legend_handles, loc="upper left")

ax.set_xlim(0.05, 2.60)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("latency_points_only_tangle_vs_caladan.png", dpi=300, bbox_inches="tight")
plt.show()