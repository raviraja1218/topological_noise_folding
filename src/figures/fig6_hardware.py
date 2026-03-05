import json
import matplotlib.pyplot as plt
import numpy as np

# Load hardware results
with open('results/hardware_real/qaoa_results.json', 'r') as f:
    data = json.load(f)

# Extract QAOA results
baseline_counts = data.get('baseline_qaoa_6q', {})
tnf_counts = data.get('tnf_qaoa_6q', {})

# Calculate optimal probabilities
optimal1, optimal2 = '010101', '101010'
baseline_opt = baseline_counts.get(optimal1, 0) + baseline_counts.get(optimal2, 0)
tnf_opt = tnf_counts.get(optimal1, 0) + tnf_counts.get(optimal2, 0)
total = 2048

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(['Baseline', 'TNF'], 
              [baseline_opt/total, tnf_opt/total],
              color=['orange', 'blue'])
ax.set_ylabel('Optimal Solution Probability')
ax.set_title('QAOA 6-Qubit on IBM Quantum Hardware')
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.4f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('figures/hardware_results.pdf', dpi=300, bbox_inches='tight')
print("✅ Figure 6 saved: figures/hardware_results.pdf")
