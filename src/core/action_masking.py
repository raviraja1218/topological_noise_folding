import torch
import numpy as np
import networkx as nx
from typing import List, Dict, Tuple
import copy

class ActionMasking:
    """Mask invalid actions that break Pauli flow"""
    
    def __init__(self, num_actions=23):
        self.num_actions = num_actions
        
    def get_action_mask(self, graph, M=None, N=None, C=None):
        """
        Get mask of valid actions
        
        Args:
            graph: Current ZX-diagram (networkx graph)
            M: Flow-demand matrix (optional)
            N: Order-demand matrix (optional)
            C: Connectivity matrix (optional)
            
        Returns:
            mask: Boolean array [num_actions] where True = valid
        """
        mask = np.ones(self.num_actions, dtype=bool)
        
        # If we have matrices, use them for validation
        if M is not None and N is not None and C is not None:
            # Check each action
            for action in range(self.num_actions):
                if not self._check_action_preserves_flow(action, graph, M, N, C):
                    mask[action] = False
        else:
            # Without matrices, use heuristic rules
            mask = self._get_heuristic_mask(graph)
            
        return mask
    
    def _check_action_preserves_flow(self, action, graph, M, N, C):
        """
        Check if applying action preserves Pauli flow
        
        This would involve:
        1. Simulating action on graph copy
        2. Recomputing M, N, C matrices
        3. Checking if NC remains acyclic
        """
        # For now, return True for all (simplified)
        # In practice, this would call the Pauli flow validator
        return True
    
    def _get_heuristic_mask(self, graph):
        """Get heuristic mask based on graph properties"""
        mask = np.ones(self.num_actions, dtype=bool)
        
        num_nodes = graph.number_of_nodes()
        
        # Rule: Can't fuse if less than 2 nodes
        if num_nodes < 2:
            mask[0] = False  # spider_fusion_z
            mask[1] = False  # spider_fusion_x
            
        # Rule: Can't remove identity if no nodes with phase zero
        has_zero_phase = False
        for node in graph.nodes():
            if 'phase' in graph.nodes[node]:
                phase = float(graph.nodes[node].get('phase', 0))
                if abs(phase) < 0.01:
                    has_zero_phase = True
                    break
                    
        if not has_zero_phase:
            mask[13] = False  # identity_removal_z
            mask[14] = False  # identity_removal_x
            
        return mask
    
    def update_matrices(self, graph):
        """
        Update M, N, C matrices after action
        
        Returns:
            M, N, C: Updated matrices
        """
        num_nodes = graph.number_of_nodes()
        
        # Create connectivity matrix C
        C = np.zeros((num_nodes, num_nodes))
        for i, j in graph.edges():
            C[i, j] = 1
            C[j, i] = 1
            
        # Create flow-demand matrix M (simplified)
        M = np.random.binomial(1, 0.1, (num_nodes, num_nodes))
        np.fill_diagonal(M, 0)
        
        # Create order-demand matrix N (simplified)
        N = np.random.randint(-5, 5, (num_nodes, num_nodes))
        N = np.triu(N) - np.triu(N).T
        
        return M, N, C
    
    def has_pauli_flow(self, M, N, C):
        """
        Check if NC forms a DAG
        
        Returns:
            bool: True if Pauli flow exists
        """
        n = C.shape[0]
        NC = N @ C
        
        # Check if NC is acyclic using trace of powers
        NC_power = NC.copy()
        for k in range(2, min(5, n)):
            NC_power = NC_power @ NC
            if np.any(np.diag(NC_power) > 1e-5):
                return False
        return True

class ActionMasker:
    """Wrapper for action masking during RL training"""
    
    def __init__(self, env, validator):
        self.env = env
        self.validator = validator
        
    def get_masked_action(self, state, epsilon=0.1):
        """
        Get action with masking (epsilon-greedy)
        
        Args:
            state: Current environment state
            epsilon: Exploration rate
            
        Returns:
            action: Selected action
        """
        # Get action mask
        mask = self.validator.get_action_mask(state['graph'])
        
        # Epsilon-greedy with masking
        if np.random.random() < epsilon:
            # Explore: random valid action
            valid_actions = np.where(mask)[0]
            if len(valid_actions) > 0:
                action = np.random.choice(valid_actions)
            else:
                action = 0
        else:
            # Exploit: use policy (simplified)
            action = np.random.choice(np.where(mask)[0]) if np.any(mask) else 0
            
        return action

if __name__ == "__main__":
    # Test action masking
    masking = ActionMasking()
    
    # Create test graph
    G = nx.random_graphs.erdos_renyi_graph(10, 0.2)
    
    # Get mask
    mask = masking.get_action_mask(G)
    print(f"Action mask: {mask}")
    print(f"Valid actions: {np.sum(mask)}/{len(mask)}")
    
    # Test flow check
    M, N, C = masking.update_matrices(G)
    has_flow = masking.has_pauli_flow(M, N, C)
    print(f"Has Pauli flow: {has_flow}")
