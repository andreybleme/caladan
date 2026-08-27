# cache_miss_counts_grouped_bar.py
# Generates a grouped bar chart of ABSOLUTE miss counts (L1, L2, LLC)
# comparing Prefetch ON vs OFF. No title, annotated with values + Δ.
# Uses only matplotlib. Saves PNG to ./cache_miss_counts_grouped_bar.png

import re
import matplotlib.pyplot as plt
import numpy as np
from textwrap import dedent

plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24

# Toggle to True for log y-axis so L1/L2 (billions) and LLC (thousands) are both visible
USE_LOG_Y = True

# ---------------------------
# Raw perf logs (paste yours if needed)
# ---------------------------
log_on = dedent("""\
Performance counter stats for './iokerneld':

   864,168,675,147      cycles
 1,708,325,963,198      instructions
   333,505,621,745      L1-dcache-loads
     4,550,721,626      L1-dcache-load-misses
     5,379,967,275      l2_rqsts.references
     2,984,001,436      l2_rqsts.miss
     1,316,206,791      LLC-loads
           142,642      LLC-load-misses
""")

log_off = dedent("""\
Performance counter stats for './iokerneld':

   867,570,100,830      cycles
 1,718,507,057,843      instructions
   335,199,345,982      L1-dcache-loads
     4,502,839,085      L1-dcache-load-misses
     5,329,867,726      l2_rqsts.references
     2,993,945,320      l2_rqsts.miss
     1,305,781,003      LLC-loads
           178,794      LLC-load-misses
""")

# ---------------------------
# Parse counters we care about
# ---------------------------
def parse_perf_block(text):
    wanted = {
        "L1-dcache-load-misses": "l1_miss",
        "l2_rqsts.miss": "l2_miss",
        "LLC-load-misses": "llc_miss",
    }
    out = {v: 0 for v in wanted.values()}
    line_re = re.compile(r"^\s*([\d,]+)\s+([A-Za-z0-9_.\-]+)")
    for line in text.splitlines():
        m = line_re.match(line)
        if not m:
            continue
        num = int(m.group(1).replace(",", ""))
        name = m.group(2)
        if name in wanted:
            out[wanted[name]] = num
    return out

on = parse_perf_block(log_on)
off = parse_perf_block(log_off)

levels = ["L1", "L2", "LLC"]
on_vals = [on["l1_miss"], on["l2_miss"], on["llc_miss"]]
off_vals = [off["l1_miss"], off["l2_miss"], off["llc_miss"]]

# ---------------------------
# Helpers
# ---------------------------
def human_int(n: int) -> str:
    """Format large ints into 1.23K / 4.56M / 7.89B strings."""
    absn = abs(n)
    if absn >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    if absn >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if absn >= 1_000:
        return f"{n/1_000:.2f}K"
    return f"{n:,}"

def pct_change(new: int, old: int) -> float:
    if old == 0:
        return 0.0
    return 100.0 * (new - old) / old

# ---------------------------
# Plot
# ---------------------------
x = np.arange(len(levels))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 4.5))

rects_on = ax.bar(x - width/2, on_vals, width, label="Prefetch ON")
rects_off = ax.bar(x + width/2, off_vals, width, label="Prefetch OFF")

ax.set_ylabel("Miss count")
ax.set_xticks(x, levels)
ax.legend(fontsize=16)

# Optional log y to keep LLC visible next to L1/L2
if USE_LOG_Y:
    ax.set_yscale("log")
    ymin = min(min(on_vals), min(off_vals))
    if ymin <= 0:
        ymin = 1
    ax.set_ylim(bottom=ymin * 0.7)

# ---------------------------
# Annotate bars (ONLY percentage, no absolute numbers)
# ---------------------------

def autolabel_pct(ax, rects, base_vals):
    """
    Annotate each bar with ONLY the percent difference
    relative to the 'base_vals' (e.g., OFF values).
    """
    for r, base in zip(rects, base_vals):
        height = r.get_height()
        pct = pct_change(height, base)
        ax.annotate(
            f"{pct:+.2f}%",
            xy=(r.get_x() + r.get_width()/2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=15,          # << bigger font size
        )

# annotate ON relative to OFF
autolabel_pct(ax, rects_on, off_vals)

# annotate OFF relative to ON (if you want OFF to be "baseline", use zeros)
autolabel_pct(ax, rects_off, on_vals)

fig.tight_layout()
out_path = "tangle_cache_miss_counts_big_fonts.pdf"
fig.savefig(out_path, dpi=200)
plt.show()
