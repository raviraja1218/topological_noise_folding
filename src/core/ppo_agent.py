import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random
from pathlib import Path

# Import Graph Transformer from Phase 3
from gnn_transformer import GraphTransformer

class PolicyNetwork(nn.Module):
    """Policy network for PPO (Graph Transformer + action head)"""
    
    def __init__(self, in_channels=32, hidden_channels=256, num_actions=23):
        super().__init__()
        
        # Graph Transformer backbone
        self.backbone = GraphTransformer(
            in_channels=in_channels,
            hidden_channels=hidden_channels,
            out_channels=hidden_channels,  # Output features, not T-count
            num_layers=6,  # Slightly smaller for faster inference
            num_heads=8,
            dropout=0.1
        )
        
        # Action head (policy)
        self.action_head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Linear(hidden_channels // 2, num_actions)
        )
        
        # Value head (critic)
        self.value_head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Linear(hidden_channels // 2, 1)
        )
        
    def forward(self, x, edge_index, edge_attr, batch):
        # Get graph embeddings
        # Note: backbone returns (tcount_pred, gamma_pred) but we ignore
        # In practice, you'd modify GraphTransformer to return embeddings
        # For now, we'll simulate
        batch_size = batch.max().item() + 1
        
        # Random embeddings for demonstration
        graph_emb = torch.randn(batch_size, 256, device=x.device)
        
        # Policy logits
        action_logits = self.action_head(graph_emb)
        
        # State values
        state_values = self.value_head(graph_emb).squeeze(-1)
        
        return action_logits, state_values

class ValueNetwork(nn.Module):
    """Value network for PPO (critic)"""
    
    def __init__(self, in_channels=32, hidden_channels=256):
        super().__init__()
        
        self.backbone = GraphTransformer(
            in_channels=in_channels,
            hidden_channels=hidden_channels,
            out_channels=hidden_channels,
            num_layers=4,  # Smaller critic
            num_heads=4,
            dropout=0.1
        )
        
        self.value_head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Linear(hidden_channels // 2, 1)
        )
        
    def forward(self, x, edge_index, edge_attr, batch):
        # Get graph embeddings
        batch_size = batch.max().item() + 1
        graph_emb = torch.randn(batch_size, 256, device=x.device)
        
        # State values
        state_values = self.value_head(graph_emb).squeeze(-1)
        
        return state_values

class PPOMemory:
    """Storage for PPO trajectories"""
    
    def __init__(self, batch_size):
        self.states = []
        self.actions = []
        self.probs = []
        self.vals = []
        self.rewards = []
        self.dones = []
        self.batch_size = batch_size
        
    def push(self, state, action, prob, val, reward, done):
        self.states.append(state)
        self.actions.append(action)
        self.probs.append(prob)
        self.vals.append(val)
        self.rewards.append(reward)
        self.dones.append(done)
        
    def clear(self):
        self.states = []
        self.actions = []
        self.probs = []
        self.vals = []
        self.rewards = []
        self.dones = []
        
    def get_batches(self):
        n = len(self.states)
        arr = np.arange(n)
        np.random.shuffle(arr)
        
        batches = []
        for start in range(0, n, self.batch_size):
            end = start + self.batch_size
            batch_indices = arr[start:end]
            batches.append(batch_indices)
            
        return batches

class PPOAgent:
    """Proximal Policy Optimization Agent"""
    
    def __init__(self, 
                 in_channels=32,
                 hidden_channels=256,
                 num_actions=23,
                 lr=3e-4,
                 gamma=0.99,
                 gae_lambda=0.95,
                 clip_epsilon=0.2,
                 value_coef=0.5,
                 entropy_coef=0.01,
                 epochs=10,
                 batch_size=64):
        
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_epsilon = clip_epsilon
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        self.epochs = epochs
        self.batch_size = batch_size
        
        # Networks
        self.policy = PolicyNetwork(in_channels, hidden_channels, num_actions)
        self.old_policy = PolicyNetwork(in_channels, hidden_channels, num_actions)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        
        # Memory
        self.memory = PPOMemory(batch_size)
        
    def select_action(self, state, mask=None):
        """Select action using current policy"""
        # For now, return random action (simplified)
        action = np.random.randint(0, 23)
        prob = 0.1
        value = 0.0
        
        return action, prob, value
    
    def update(self):
        """Update policy using PPO"""
        # Simplified update for now
        pass
    
    def save(self, path):
        """Save model checkpoint"""
        torch.save({
            'policy_state_dict': self.policy.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, path)
        print(f"✅ Model saved to {path}")
        
    def load(self, path):
        """Load model checkpoint"""
        checkpoint = torch.load(path)
        self.policy.load_state_dict(checkpoint['policy_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print(f"✅ Model loaded from {path}")

if __name__ == "__main__":
    # Test the agent
    agent = PPOAgent()
    print(f"PPO Agent created with {sum(p.numel() for p in agent.policy.parameters()):,} parameters")
    
    # Test action selection
    action, prob, value = agent.select_action(None)
    print(f"Sample action: {action}, prob: {prob:.2f}, value: {value:.2f}")
