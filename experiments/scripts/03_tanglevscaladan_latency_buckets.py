import pandas as pd
import matplotlib.pyplot as plt

# Path to your log file (save the sample data into 'sample.log')
log_file = '../baseline/start 0.005 - mpps 4.0 - bimodal 0.90:83:918/synthetic_buckets.log'
log_file_tangle = '../tangle/start 0.005 - mpps 4.0 - bimodal 0.90:83:918/synthetic_buckets.log'
#log_file = '../baseline/start 0.005 - mpps 4.0/synthetic_buckets.log'

# Parse the "Latencies:" lines and build a latency→count mapping
buckets = {}
with open(log_file_tangle, 'r') as f:
    for line in f:
        if line.startswith('Latencies:'):
            # strip off the "Latencies: " prefix, split into "latency:count" tokens
            entries = line[len('Latencies: '):].split()
            for token in entries:
                latency_str, count_str = token.split(':')
                latency = int(latency_str)
                count   = int(count_str)
                buckets[latency] = buckets.get(latency, 0) + count

# Turn into a sorted DataFrame
df = pd.DataFrame.from_dict(buckets, orient='index', columns=['count'])
df.index.name = 'latency_us'
df = df.reset_index().sort_values('latency_us')


# Plot histogram (bar chart)
# plt.figure(figsize=(10, 6))
# plt.bar(df['latency_us'], df['count'], width=1.0, edgecolor='black')
# plt.xlabel('Latency (µs)')
# plt.ylabel('Packet count')
# plt.title('Packet‑Latency Distribution Histogram')
# plt.xticks(df['latency_us'][::10], rotation=45)  # show every 10th tick for readability
# plt.tight_layout()

# Coarse‑binning (bucket aggregation)
BIN_SIZE = 5  # µs per new bucket
df['bin_floor'] = (df['latency_us'] // BIN_SIZE) * BIN_SIZE

# aggregate counts per coarse bin
agg = df.groupby('bin_floor')['count'].sum().reset_index()

plt.figure(figsize=(8,5))
plt.bar(agg['bin_floor'], agg['count'], width=BIN_SIZE, edgecolor='black')
plt.xlabel(f'Latency (µs) (binned by {BIN_SIZE} µs)')
plt.ylabel('Packet count')
plt.title(f'Coarse‑binned (​{BIN_SIZE} µs) latency histogram')
plt.tight_layout()

# Save the plot to a file
plt.savefig("tangle_buckets_bimodal.png")
