"""
Visualize circuit routing on device topology
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_circuit_layout
from device_topologies import get_coupling_map

class RoutingVisualizer:
    def __init__(self, device_name='ibm_fez'):
        self.device = get_coupling_map(device_name)
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.device['coupling'])
        
    def plot_topology(self, save_path='figures/device_topology.pdf'):
        """Plot the device coupling map"""
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue',
                node_size=500, font_size=8, font_weight='bold')
        plt.title(f"{self.device['name']} - {self.device['qubits']} Qubits")
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Topology saved to {save_path}")
    
    def visualize_routing(self, circuit, filename='routing.pdf'):
        """Show how circuit maps to device"""
        from qiskit import IBMQ
        from qiskit.providers.fake_provider import FakeProvider
        
        # Create fake backend for visualization
        fake_provider = FakeProvider()
        backend = fake_provider.get_backend('fake_santiago')
        
        # Transpile for backend
        transpiled = transpile(circuit, backend=backend, optimization_level=3)
        
        # Plot layout
        fig = plot_circuit_layout(transpiled, backend)
        fig.savefig(f'figures/{filename}', dpi=300, bbox_inches='tight')
        print(f"✅ Routing saved to figures/{filename}")
    
    def compare_routing(self, baseline_circuit, tnf_circuit):
        """Side-by-side comparison"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Layout for baseline
        pos = nx.spring_layout(self.graph, seed=42)
        
        # Plot baseline routing (simplified)
        nx.draw(self.graph, pos, ax=axes[0], node_color='lightblue',
                node_size=300, with_labels=False)
        axes[0].set_title('Baseline Circuit Routing')
        
        # Plot TNF routing
        nx.draw(self.graph, pos, ax=axes[1], node_color='lightgreen',
                node_size=300, with_labels=False)
        axes[1].set_title('TNF-Optimized Routing')
        
        plt.tight_layout()
        plt.savefig('figures/routing_comparison.pdf', dpi=300, bbox_inches='tight')
        print("✅ Routing comparison saved")

if __name__ == "__main__":
    viz = RoutingVisualizer('ibm_fez')
    viz.plot_topology()
    
    # Test circuit
    qc = QuantumCircuit(5)
    qc.cx(0, 4)
    qc.cx(1, 3)
    viz.visualize_routing(qc, 'test_routing.pdf')
