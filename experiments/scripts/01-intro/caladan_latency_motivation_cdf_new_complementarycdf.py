# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from io import StringIO
# from matplotlib.colors import Normalize
# from matplotlib.cm import ScalarMappable

# DATA = """Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
# zero, 129567, 129567, 0, 7201, 12.0, 18.0, 22.0, 169.0, 238.0, 1744810262, 4517905260852237
# zero, 254181, 254181, 0, 9251, 11.0, 15.0, 21.0, 170.0, 237.0, 1744810283, 4517955449645319
# zero, 378845, 378845, 0, 11852, 12.0, 16.0, 23.0, 195.0, 259.0, 1744810305, 4518007910689680
# zero, 503472, 503472, 0, 14078, 12.0, 15.0, 21.0, 208.0, 265.0, 1744810328, 4518062754739965
# zero, 627959, 627959, 0, 17147, 12.0, 15.0, 20.0, 228.0, 260.0, 1744810351, 4518119369184468
# zero, 752338, 752338, 0, 20058, 12.0, 15.0, 22.0, 234.0, 270.0, 1744810376, 4518178029876939
# zero, 877382, 877382, 0, 79767, 13.0, 16.0, 38.0, 239.0, 264.0, 1744810401, 4518238880193495
# zero, 1001474, 1001474, 0, 1036711, 13.0, 15.0, 71.0, 259.0, 287.0, 1744810427, 4518300323709195
# zero, 1125116, 1125116, 0, 3168678, 13.0, 15.0, 40.0, 255.0, 285.0, 1744810454, 4518363926345751
# zero, 1250789, 1250789, 0, 6215828, 12.0, 15.0, 27.0, 346.0, 379.0, 1744810481, 4518430060809333
# zero, 1367417, 1367417, 0, 7261295, 12.0, 15.0, 24.0, 319.0, 380.0, 1744810510, 4518497950144125
# zero, 1497120, 1497120, 0, 10478303, 12.0, 15.0, 25.0, 302.0, 356.0, 1744810539, 4518567627061170
# zero, 1598351, 1598351, 0, 12371483, 12.0, 15.0, 28.0, 336.0, 397.0, 1744810570, 4518641465034459
# zero, 1733612, 1733612, 0, 13152188, 12.0, 14.0, 21.0, 241.0, 262.0, 1744810600, 4518713789232357
# zero, 1779053, 1779053, 0, 15322467, 12.0, 14.0, 24.0, 249.0, 279.0, 1744810632, 4518791716504689
# zero, 1803118, 1803118, 0, 17166512, 12.0, 14.0, 21.0, 237.0, 261.0, 1744810665, 4518870332741106
# zero, 1822368, 1822368, 0, 19309612, 12.0, 14.0, 21.0, 249.0, 279.0, 1744810699, 4518951258380769
# zero, 1847202, 1847202, 0, 22348730, 12.0, 14.0, 20.0, 268.0, 429.0, 1744810733, 4519032088527924
# zero, 1904369, 1904369, 0, 23548424, 12.0, 14.0, 21.0, 300.0, 535.0, 1744810767, 4519114951642887
# zero, 1964553, 1964553, 0, 26450091, 12.0, 15.0, 27.0, 359.0, 629.0, 1744810803, 4519200873455925"""

# # Normalize the header.
# header = (
#     "Distribution,Target,Actual,Dropped,Never Sent,"
#     "Median,90th,99th,99.9th,99.99th,Start,StartTsc"
# )

# lines = DATA.strip().splitlines()
# lines[0] = header

# df = pd.read_csv(
#     StringIO("\n".join(lines)),
#     skipinitialspace=True
# )

# # Available percentile measurements.
# percentile_cols = ["Median", "90th", "99th", "99.9th", "99.99th"]

# # Probability represented by each percentile.
# cdf_probabilities = np.array([
#     0.50,    # Median
#     0.90,    # 90th
#     0.99,    # 99th
#     0.999,   # 99.9th
#     0.9999   # 99.99th
# ])

# # CCDF = 1 - CDF.
# tail_probabilities = 1.0 - cdf_probabilities

# fig, ax = plt.subplots(figsize=(8, 5))

# # Use color to represent the actual achieved throughput.
# norm = Normalize(
#     vmin=df["Actual"].min(),
#     vmax=df["Actual"].max()
# )
# cmap = plt.colormaps["viridis"]

# for _, row in df.iterrows():
#     latencies = row[percentile_cols].to_numpy(dtype=float)
#     color = cmap(norm(row["Actual"]))

#     ax.plot(
#         latencies,
#         tail_probabilities,
#         color=color,
#         linewidth=1.5,
#         marker="o",
#         markersize=3,
#         alpha=0.75
#     )

# # Logarithmic tail-probability axis.
# ax.set_yscale("log")

# ax.set_xlabel("Latency (µs)", fontsize=16)
# ax.set_ylabel("Fraction of packets with latency > x", fontsize=14)

# ax.set_ylim(1e-4, 1)
# ax.set_yticks([1, 1e-1, 1e-2, 1e-3, 1e-4])

# ax.grid(
#     True,
#     which="both",
#     linestyle="--",
#     linewidth=0.6,
#     alpha=0.7
# )

# # Color bar identifying the load of each curve.
# sm = ScalarMappable(norm=norm, cmap=cmap)
# sm.set_array([])

# cbar = fig.colorbar(sm, ax=ax)
# cbar.set_label("Actual throughput (packets/s)", fontsize=12)

# plt.tight_layout()
# plt.savefig(
#     "motivation_caladan_latency_complementary_cdf.pdf",
#     dpi=160,
#     bbox_inches="tight"
# )
# plt.show()


# ============== ============== ============== to show one opeating point ============== ============== ==============
# ============== ============== ============== to show one opeating point ============== ============== ==============

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

DATA = """Distribution, Target, Actual, Dropped, Never Sent, Median, 90th, 99th, 99.9th, 99.99th, Start, StartTsc
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
zero, 1964553, 1964553, 0, 26450091, 12.0, 15.0, 27.0, 359.0, 629.0, 1744810803, 4519200873455925"""

header = (
    "Distribution,Target,Actual,Dropped,Never Sent,"
    "Median,90th,99th,99.9th,99.99th,Start,StartTsc"
)

lines = DATA.strip().splitlines()
lines[0] = header

df = pd.read_csv(
    StringIO("\n".join(lines)),
    skipinitialspace=True
)

percentile_cols = ["Median", "90th", "99th", "99.9th", "99.99th"]

tail_probabilities = np.array([
    0.5,
    0.1,
    0.01,
    0.001,
    0.0001
])

# Select the experiment with the highest actual throughput.
row = df.loc[df["Actual"].idxmax()]
latencies = row[percentile_cols].to_numpy(dtype=float)

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    latencies,
    tail_probabilities,
    color="steelblue",
    linewidth=2,
    marker="o",
    markersize=6,
    label='Caladan Latency'
)

ax.set_yscale("log")
ax.set_ylim(1e-4, 1)

ax.set_xlabel("Latency (µs)", fontsize=16)
ax.set_ylabel("Fraction of packets with latency > x", fontsize=14)

ax.grid(
    True,
    which="both",
    linestyle="--",
    linewidth=0.6,
    alpha=0.7
)

ax.legend(fontsize=13)
plt.tight_layout()

plt.savefig(
    "motivation_caladan_latency_ccdf.pdf",
    dpi=160,
    bbox_inches="tight"
)
plt.show()

# ============== ============== ============== to show per packet latency logs ============== ============== ==============
# ============== ============== ============== to show per packet latency logs ============== ============== ==============

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# df = pd.read_csv("packet_latencies.csv")

# latencies = df["latency_us"].dropna().to_numpy(dtype=float)
# latencies = np.sort(latencies)

# n = len(latencies)

# # Empirical survival probability P(X >= x).
# # It finishes at 1/n rather than zero, which is necessary
# # because zero cannot be displayed on a logarithmic axis.
# ccdf = (n - np.arange(n)) / n

# fig, ax = plt.subplots(figsize=(8, 5))

# ax.step(
#     latencies,
#     ccdf,
#     where="post",
#     color="steelblue",
#     linewidth=2,
#     label="Caladan latency"
# )

# ax.set_yscale("log")

# ax.set_xlabel("Latency (µs)", fontsize=16)
# ax.set_ylabel("Fraction of packets with latency ≥ x", fontsize=14)

# ax.grid(
#     True,
#     which="both",
#     linestyle="--",
#     linewidth=0.6,
#     alpha=0.7
# )

# ax.legend(fontsize=14)
# plt.tight_layout()

# plt.savefig(
#     "motivation_caladan_latency_ccdf.pdf",
#     dpi=160,
#     bbox_inches="tight"
# )
# plt.show()