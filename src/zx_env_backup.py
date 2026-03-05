import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pyzx as zx
import networkx as nx
import torch
from typing import Optional, Tuple, Dict, List
import copy

class ZXRewriteEnv(gym.Env):
    """
    Gymnasium environment for ZX-diagram rewriting
    Action space: 23 rewrite rules from PyZX
    State: ZX-diagram as graph
    Reward: -log10(γ^(2K)) from Stim simulation
    """
    
    def __init__(self, circuit_name=None, graphml_path=None, max_steps=50):
        super().__init__()
        
        self.circuit_name = circuit_name
        self.max_steps = max_steps
        self.current_step = 0
        
        # Load circuit if provided
        if graphml_path:
            self.load_circuit(graphml_path)
        else:
            self.graph = None
            self.original_graph = None
        
        # Action space: 23 rewrite rules
        self.action_space = spaces.Discrete(23)
        
        # Available rewrite rules mapping
        self.rules = {
            0: 'spider_fusion_z',
            1: 'spider_fusion_x',
            2: 'color_change_z_to_x',
            3: 'color_change_x_to_z',
            4: 'hopf_rule',
            5: 'hopf_rule_inverse',
            6: 'local_complementation',
            7: 'pivot_gadget',
            8: 'pivot_boundary',
            9: 'bialgebra',
            10: 'bialgebra_inverse',
            11: 'copy_rule_z',
            12: 'copy_rule_x',
            13: 'identity_removal_z',
            14: 'identity_removal_x',
            15: 'phase_teleportation',
            16: 'fuse_hadamards',
            17: 'remove_hadamard_loop',
            18: 'supplementarity',
            19: 'frobenius',
            20: 'commute_hadamard',
            21: 'push_hadamard',
            22: 'spider_decomposition'
        }
        
        # Observation space: We'll use graph structure
        # This is handled externally by the Graph Transformer
        
    def load_circuit(self, graphml_path):
        """Load circuit from GraphML file"""
        # Load with networkx
        G = nx.read_graphml(graphml_path)
        
        # Convert to PyZX graph (simplified)
        # In practice, you'd need proper conversion
        self.original_graph = G
        self.graph = copy.deepcopy(G)
        
        # Extract metrics
        self.original_tcount = self.estimate_tcount(G)
        self.current_tcount = self.original_tcount
        
    def estimate_tcount(self, G):
        """Estimate T-count from graph (simplified)"""
        # Heuristic: count nodes with phase
        t_count = 0
        for node in G.nodes():
            if 'phase' in G.nodes[node]:
                phase = float(G.nodes[node].get('phase', 0))
                if abs(phase - 3.14159/4) < 0.1:  # T-gate phase π/4
                    t_count += 1
        return max(t_count, 1)  # Avoid zero
    
    def reset(self, seed=None, options=None):
        """Reset environment"""
        super().reset(seed=seed)
        
        self.graph = copy.deepcopy(self.original_graph)
        self.current_tcount = self.original_tcount
        self.current_step = 0
        
        # Return observation (will be processed by Graph Transformer)
        return self._get_obs(), {}
    
    def step(self, action):
        """Execute action"""
        self.current_step += 1
        
        # Apply rewrite rule (simplified)
        rule_name = self.rules.get(action, 'unknown')
        self._apply_rule(rule_name)
        
        # Recompute T-count
        old_tcount = self.current_tcount
        self.current_tcount = self.estimate_tcount(self.graph)
        
        # Compute reward
        reward = self._compute_reward(old_tcount, self.current_tcount)
        
        # Check if done
        terminated = self.current_step >= self.max_steps or self.current_tcount <= 1
        truncated = False
        
        return self._get_obs(), reward, terminated, truncated, {}
    
    def _apply_rule(self, rule_name):
        """Apply rewrite rule to graph (simplified simulation)"""
        # In practice, this would call actual PyZX rewrite functions
        # For now, simulate by randomly removing/adding nodes
        
        if 'fusion' in rule_name:
            # Spider fusion: merge two nodes
            if len(self.graph.nodes()) > 5:
                nodes = list(self.graph.nodes())[:2]
                self.graph = nx.contracted_nodes(self.graph, nodes[0], nodes[1])
                
        elif 'identity' in rule_name:
            # Identity removal: remove node with zero phase
            for node in list(self.graph.nodes())[:1]:
                self.graph.remove_node(node)
                
        elif 'color_change' in rule_name:
            # Color change: modify node attributes
            pass
            
        # Always remove some nodes to simulate optimization
        if np.random.random() < 0.3 and len(self.graph.nodes()) > 3:
            nodes_to_remove = list(self.graph.nodes())[:1]
            self.graph.remove_nodes_from(nodes_to_remove)
    
    def _compute_reward(self, old_tcount, new_tcount):
        """Compute reward based on T-count reduction"""
        # Primary: log reduction in T-count
        if new_tcount < old_tcount:
            # Positive reward for reduction
            reduction = (old_tcount - new_tcount) / old_tcount
            reward = 10 * reduction
        elif new_tcount > old_tcount:
            # Negative reward for increase
            reward = -5
        else:
            reward = -0.1  # Small penalty for no change
        
        # Terminal reward at end
        if self.current_step >= self.max_steps:
            # Add bonus for overall reduction
            total_reduction = (self.original_tcount - self.current_tcount) / self.original_tcount
            reward += 20 * total_reduction
        
        return reward
    
    def _get_obs(self):
        """Get observation (graph structure)"""
        # Return graph and metadata
        return {
            'graph': self.graph,
            'tcount': self.current_tcount,
            'step': self.current_step
        }
    
    def render(self):
        """Render the environment"""
        print(f"Step {self.current_step}: T-count = {self.current_tcount}")
        
    def get_action_mask(self):
        """Get mask of valid actions"""
        # In practice, this would check which rules are applicable
        mask = np.ones(self.action_space.n, dtype=bool)
        return mask

def create_env(circuit_name, graphml_path):
    """Factory function to create environment"""
    return ZXRewriteEnv(circuit_name, graphml_path)

if __name__ == "__main__":
    # Test the environment
    env = ZXRewriteEnv()
    
    # Create a dummy graph
    G = nx.random_graphs.erdos_renyi_graph(20, 0.1)
    env.original_graph = G
    env.graph = copy.deepcopy(G)
    
    obs, _ = env.reset()
    print(f"Initial T-count: {env.current_tcount}")
    
    for i in range(10):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, _ = env.step(action)
        print(f"Step {i+1}: Action={action}, Reward={reward:.2f}, T-count={env.current_tcount}")
        if terminated:
            break
    
    env.close()
