import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Use Nature-style plotting
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

# Load data
df = pd.read_csv('results/ppo_training_complete.csv')
episodes = df.index + 1

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 1. Reward (Main plot)
axes[0,0].plot(episodes, df['reward'], 'b-', linewidth=1.5, alpha=0.7)
axes[0,0].fill_between(episodes, 
                       df['reward'] - df['reward'].rolling(50).std(),
                       df['reward'] + df['reward'].rolling(50).std(),
                       alpha=0.2, color='blue')
axes[0,0].axhline(y=df['reward'].iloc[-100:].mean(), color='r', linestyle='--', 
                  alpha=0.5, label=f'Final mean: {df["reward"].iloc[-100:].mean():.1f}')
axes[0,0].set_xlabel('Episode')
axes[0,0].set_ylabel('Average Reward')
axes[0,0].set_title('(a) PPO Training Reward')
axes[0,0].legend(loc='lower right')
axes[0,0].grid(True, alpha=0.3)

# 2. Entropy (Exploration vs Exploitation)
axes[0,1].plot(episodes, df['policy_entropy'], 'g-', linewidth=1.5, alpha=0.7)
axes[0,1].axhline(y=0.1, color='r', linestyle='--', alpha=0.5, label='Optimal range')
axes[0,1].fill_between([0, 400], 0.05, 0.15, alpha=0.1, color='green')
axes[0,1].set_xlabel('Episode')
axes[0,1].set_ylabel('Policy Entropy')
axes[0,1].set_title('(b) Exploration-Exploitation Trade-off')
axes[0,1].legend(loc='upper right')
axes[0,1].grid(True, alpha=0.3)

# 3. KL Divergence (Update Stability)
axes[1,0].plot(episodes, df['kl_divergence'], 'm-', linewidth=1.5, alpha=0.7)
axes[1,0].axhline(y=0.01, color='r', linestyle='--', alpha=0.5, label='Stability threshold')
axes[1,0].set_xlabel('Episode')
axes[1,0].set_ylabel('KL Divergence')
axes[1,0].set_title('(c) Policy Update Stability')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)
axes[1,0].set_yscale('log')

# 4. Explained Variance (Value Learning)
axes[1,1].plot(episodes, df['explained_variance'], 'c-', linewidth=1.5, alpha=0.7)
axes[1,1].axhline(y=0.85, color='r', linestyle='--', alpha=0.5, label='Good threshold')
axes[1,1].fill_between([0, 400], 0.85, 1.0, alpha=0.1, color='green')
axes[1,1].set_xlabel('Episode')
axes[1,1].set_ylabel('Explained Variance')
axes[1,1].set_title('(d) Value Function Accuracy')
axes[1,1].legend(loc='lower right')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/paper_training_curves.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/paper_training_curves.png', dpi=300, bbox_inches='tight')
print("✅ Paper-ready training plots saved to figures/paper_training_curves.pdf")

# Summary statistics for paper
print("\n📊 PAPER-READY TRAINING STATISTICS:")
print(f"   • Final average reward: {df['reward'].iloc[-100:].mean():.2f} ± {df['reward'].iloc[-100:].std():.2f}")
print(f"   • Policy entropy (final): {df['policy_entropy'].iloc[-1]:.3f} (optimal range: 0.05-0.15)")
print(f"   • Average KL divergence: {df['kl_divergence'].mean():.4f} (<0.01 indicates stable updates)")
print(f"   • Explained variance: {df['explained_variance'].iloc[-1]:.3f} (>0.85 indicates good value learning)")
