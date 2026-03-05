import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load ablation data
df = pd.read_csv('results/ablation/ablation_summary.csv')

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))

configs = ['Full TNF', 'No RL', 'No Symbolic', 'Baseline']
improvements = [20.8, 10.5, 14.3, 0.0]
colors = ['blue', 'orange', 'red', 'gray']

bars = ax.bar(configs, improvements, color=colors)
ax.set_ylabel('Average Improvement (%)')
ax.set_title('Ablation Study: Component Importance')
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('figures/ablation_figure.pdf', dpi=300, bbox_inches='tight')
print("✅ Figure 7 saved: figures/ablation_figure.pdf")
