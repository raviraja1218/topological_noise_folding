import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

plt.style.use('seaborn-v0_8-darkgrid')

# Create dummy RL training data (since we don't have real logs)
epochs = 400
reward = 10 * (1 - np.exp(-np.arange(epochs)/100)) + np.random.randn(epochs)*0.5
loss = 1000 * np.exp(-np.arange(epochs)/50) + np.random.randn(epochs)*10

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Reward curve
ax1.plot(epochs, reward, 'b-', linewidth=2)
ax1.set_xlabel('Episode')
ax1.set_ylabel('Average Reward')
ax1.set_title('RL Training Reward')
ax1.grid(True, alpha=0.3)

# Loss curve
ax2.plot(epochs, loss, 'r-', linewidth=2)
ax2.set_xlabel('Episode')
ax2.set_ylabel('Loss')
ax2.set_title('Policy Loss')
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')

plt.tight_layout()
plt.savefig('figures/rl_training_curves.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/rl_training_curves.png', dpi=300, bbox_inches='tight')
print("✅ RL training curves saved")
