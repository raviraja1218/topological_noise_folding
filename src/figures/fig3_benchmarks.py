import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load benchmark data
df = pd.read_csv('results/benchmarks/full_benchmark_results.csv')

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot improvements
families = df['family'].unique()
x = np.arange(len(families))
width = 0.25

tket_means = [df[df['family']==f]['tket_improvement'].mean() for f in families]
tnf_means = [df[df['family']==f]['tnf_improvement'].mean() for f in families]

ax.bar(x - width/2, tket_means, width, label='TKET', color='orange')
ax.bar(x + width/2, tnf_means, width, label='TNF', color='blue')

ax.set_xlabel('Circuit Family')
ax.set_ylabel('Average Improvement (%)')
ax.set_title('TNF vs TKET Benchmark Comparison')
ax.set_xticks(x)
ax.set_xticklabels(families, rotation=45)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/benchmark_comparison.pdf', dpi=300, bbox_inches='tight')
print("✅ Figure 3 saved: figures/benchmark_comparison.pdf")
