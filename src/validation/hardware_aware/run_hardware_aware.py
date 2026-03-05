"""
Main script to run hardware-aware analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from qiskit import QuantumCircuit

from device_topologies import list_devices, get_coupling_map
from connectivity_penalty import ConnectivityPenalty
from hardware_reward import HardwareAwareReward
from routing_visualizer import RoutingVisualizer

class HardwareAwareAnalyzer:
    def __init__(self):
        self.results = []
        
    def load_test_circuits(self):
        """Create test circuits with different routing patterns"""
        circuits = []
        
        # Circuit 1: Well-routed linear chain
        qc1 = QuantumCircuit(5)
        for i in range(4):
            qc1.cx(i, i+1)
        circuits.append(('linear_chain', qc1))
        
        # Circuit 2: Poorly-routed (long-range)
        qc2 = QuantumCircuit(5)
        qc2.cx(0, 4)
        qc2.cx(1, 3)
        circuits.append(('long_range', qc2))
        
        # Circuit 3: Star pattern
        qc3 = QuantumCircuit(5)
        for i in range(1, 5):
            qc3.cx(0, i)
        circuits.append(('star', qc3))
        
        # Circuit 4: Dense connectivity
        qc4 = QuantumCircuit(4)
        for i in range(4):
            for j in range(i+1, 4):
                qc4.cx(i, j)
        circuits.append(('dense', qc4))
        
        return circuits
    
    def analyze_device(self, device_name, circuits):
        """Analyze all circuits on a specific device"""
        penalty = ConnectivityPenalty(device_name)
        results = []
        
        for name, circuit in circuits:
            swap_count = penalty.calculate_swap_count(circuit)
            distance = penalty.calculate_distance_penalty(circuit)
            
            results.append({
                'circuit': name,
                'device': device_name,
                'swap_penalty': swap_count,
                'distance_penalty': distance
            })
        
        return pd.DataFrame(results)
    
    def analyze_all_devices(self):
        """Run analysis on all devices"""
        circuits = self.load_test_circuits()
        all_results = []
        
        for device in list_devices():
            print(f"\n📡 Analyzing {device}...")
            df = self.analyze_device(device, circuits)
            all_results.append(df)
        
        return pd.concat(all_results)
    
    def save_results(self, df):
        """Save results to file"""
        Path("results/hardware_aware").mkdir(exist_ok=True)
        
        # Save CSV
        df.to_csv("results/hardware_aware/routing_costs.csv", index=False)
        
        # Generate summary
        summary = df.groupby('device').agg({
            'swap_penalty': ['mean', 'max'],
            'distance_penalty': ['mean', 'max']
        })
        summary.to_csv("results/hardware_aware/routing_summary.csv")
        
        print("\n✅ Results saved to results/hardware_aware/")
        return summary

def main():
    print("="*60)
    print("🔧 HARDWARE-AWARE COMPILATION ANALYSIS")
    print("="*60)
    
    analyzer = HardwareAwareAnalyzer()
    
    # Run analysis
    df = analyzer.analyze_all_devices()
    summary = analyzer.save_results(df)
    
    print("\n📊 Routing Penalty Summary:")
    print(summary)
    
    # Generate visualizations
    viz = RoutingVisualizer('ibm_fez')
    viz.plot_topology('figures/ibm_fez_topology.pdf')
    
    # Compare circuits on ibm_fez
    penalty = ConnectivityPenalty('ibm_fez')
    circuits = analyzer.load_test_circuits()
    
    results = []
    for name, circuit in circuits[:2]:  # First two circuits
        swap_count = penalty.calculate_swap_count(circuit)
        results.append({'circuit': name, 'swaps': swap_count})
    
    # Create comparison plot
    import matplotlib.pyplot as plt
    names = [r['circuit'] for r in results]
    swaps = [r['swaps'] for r in results]
    
    plt.figure(figsize=(8, 6))
    plt.bar(names, swaps, color=['orange', 'blue'])
    plt.ylabel('Estimated SWAP Gates Needed')
    plt.title('Routing Cost Comparison on ibm_fez')
    plt.grid(True, alpha=0.3)
    plt.savefig('figures/routing_comparison.pdf', dpi=300, bbox_inches='tight')
    
    print("\n✅ All hardware-aware analyses complete!")

if __name__ == "__main__":
    main()
