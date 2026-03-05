"""
Modified reward function with routing penalties
"""

import numpy as np
from connectivity_penalty import ConnectivityPenalty

class HardwareAwareReward:
    def __init__(self, device_name='ibm_fez', lambda_penalty=0.1):
        self.penalty_calculator = ConnectivityPenalty(device_name)
        self.lambda_penalty = lambda_penalty
        
    def calculate_reward(self, circuit, base_reward):
        """
        R_total = R_main - λ * routing_penalty
        """
        # Calculate routing penalty
        swap_penalty = self.penalty_calculator.calculate_penalty(circuit, method='swap')
        
        # Normalize penalty (cap at 100)
        normalized_penalty = min(swap_penalty / 10, 100)
        
        # Apply penalty
        final_reward = base_reward - self.lambda_penalty * normalized_penalty
        
        return {
            'base_reward': base_reward,
            'routing_penalty': normalized_penalty,
            'swap_count': swap_penalty,
            'final_reward': final_reward
        }
    
    def compare_rewards(self, baseline_circuit, tnf_circuit, base_reward=100):
        """Compare baseline vs TNF with routing penalties"""
        baseline = self.calculate_reward(baseline_circuit, base_reward)
        tnf = self.calculate_reward(tnf_circuit, base_reward)
        
        return {
            'baseline': baseline,
            'tnf': tnf,
            'improvement': tnf['final_reward'] - baseline['final_reward']
        }

if __name__ == "__main__":
    from qiskit import QuantumCircuit
    
    # Create test circuits
    qc1 = QuantumCircuit(5)
    qc1.cx(0, 1)
    qc1.cx(1, 2)
    qc1.cx(2, 3)
    
    qc2 = QuantumCircuit(5)
    qc2.cx(0, 4)  # Bad routing
    
    reward = HardwareAwareReward()
    print("Well-routed circuit:", reward.calculate_reward(qc1, 100))
    print("Poorly-routed circuit:", reward.calculate_reward(qc2, 100))
