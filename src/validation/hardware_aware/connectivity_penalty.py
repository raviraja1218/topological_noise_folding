"""
Calculate routing penalties for circuits on specific devices
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap
import networkx as nx

class ConnectivityPenalty:
    def __init__(self, device_name='ibm_fez'):
        from device_topologies import get_coupling_map
        self.device = get_coupling_map(device_name)
        self.coupling_list = self.device['coupling']
        self.n_qubits = self.device['qubits']
        
        # Create graph for shortest path calculations
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.coupling_list)
        
    def calculate_swap_count(self, circuit):
        """Estimate number of SWAP gates needed for routing"""
        swap_count = 0
        
        # Get all 2-qubit gates
        for instruction in circuit.data:
            if instruction.operation.name == 'cx':
                q1 = instruction.qubits[0].index
                q2 = instruction.qubits[1].index
                
                # Check if directly connected
                if (q1, q2) not in self.coupling_list and (q2, q1) not in self.coupling_list:
                    # Find shortest path
                    try:
                        path = nx.shortest_path(self.graph, q1, q2)
                        # Each edge in path requires SWAP
                        swap_count += len(path) - 1
                    except:
                        swap_count += 10  # Large penalty if disconnected
        
        return swap_count
    
    def calculate_distance_penalty(self, circuit):
        """Penalty based on physical distance between qubits"""
        total_distance = 0
        
        for instruction in circuit.data:
            if instruction.operation.name == 'cx':
                q1 = instruction.qubits[0].index
                q2 = instruction.qubits[1].index
                
                try:
                    path = nx.shortest_path(self.graph, q1, q2)
                    total_distance += len(path) - 1
                except:
                    total_distance += 100
        
        return total_distance
    
    def calculate_penalty(self, circuit, method='swap'):
        """Combined penalty score"""
        if method == 'swap':
            return self.calculate_swap_count(circuit)
        elif method == 'distance':
            return self.calculate_distance_penalty(circuit)
        else:
            return 0
    
    def compare_circuits(self, baseline_circuit, tnf_circuit):
        """Compare routing cost between baseline and TNF"""
        baseline_penalty = self.calculate_penalty(baseline_circuit)
        tnf_penalty = self.calculate_penalty(tnf_circuit)
        
        return {
            'baseline_penalty': baseline_penalty,
            'tnf_penalty': tnf_penalty,
            'improvement': (baseline_penalty - tnf_penalty) / max(1, baseline_penalty) * 100,
            'baseline_better': tnf_penalty < baseline_penalty
        }

if __name__ == "__main__":
    # Test with simple circuit
    from qiskit import QuantumCircuit
    
    qc = QuantumCircuit(5)
    qc.cx(0, 4)  # Far apart qubits
    qc.cx(1, 2)  # Likely connected
    
    penalty = ConnectivityPenalty('ibm_fez')
    swaps = penalty.calculate_swap_count(qc)
    print(f"Estimated SWAP gates needed: {swaps}")
