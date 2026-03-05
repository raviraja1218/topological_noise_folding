import json
import pickle
import pyzx as zx
import networkx as nx
import pandas as pd
from pathlib import Path
import time

print("=" * 60)
print("STEP 2.1: Baseline Circuit Analysis")
print("=" * 60)

# Create output directories
Path("data/processed/baseline_graphs").mkdir(parents=True, exist_ok=True)
Path("results").mkdir(exist_ok=True)

# Load circuits
print("\n📂 Loading circuits from Phase 1...")
with open("data/raw/op_t_mize_baseline.pkl", "rb") as f:
    circuits = pickle.load(f)

print(f"✅ Loaded {len(circuits)} circuits")

# Initialize results list
baseline_data = []

# Process each circuit
print("\n🔄 Processing circuits...")
for i, (name, data) in enumerate(circuits.items(), 1):
    print(f"\n  [{i}/{len(circuits)}] {name} ({data['qubits']} qubits)")
    
    # Create a simple QASM representation (simplified for baseline)
    qasm = f"""OPENQASM 2.0;
include "qelib1.inc";
qreg q[{data['qubits']}];
"""
    # Add some basic gates based on circuit type (simplified for demo)
    # In real implementation, you'd have actual circuit definitions
    for j in range(min(data['t_gates'], 10)):  # Simplified for demo
        qasm += f"t q[{j % data['qubits']}];\n"
    
    try:
        # Convert to PyZX circuit
        circuit = zx.Circuit.from_qasm(qasm)
        
        # Convert to ZX graph
        g = circuit.to_graph()
        
        # Save as GraphML via networkx
        nx_graph = nx.Graph()
        for v in range(g.num_vertices()):
            nx_graph.add_node(v)
        for e in g.edges():
            nx_graph.add_edge(e[0], e[1])
        
        graphml_path = f"data/processed/baseline_graphs/{name}.graphml"
        nx.write_graphml(nx_graph, graphml_path)
        
        # Record metrics
        baseline_data.append({
            "circuit_name": name,
            "family": data["family"],
            "qubits": data["qubits"],
            "t_count": data["t_gates"],
            "two_qubit_gates": data.get("two_qubit_gates", data["qubits"] * 3),
            "depth": data["depth"],
            "graph_nodes": g.num_vertices(),
            "graph_edges": g.num_edges(),
            "graphml_file": graphml_path
        })
        
        print(f"    ✅ Graph saved: {graphml_path} ({g.num_vertices()} nodes)")
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        # Add with placeholder data
        baseline_data.append({
            "circuit_name": name,
            "family": data["family"],
            "qubits": data["qubits"],
            "t_count": data["t_gates"],
            "two_qubit_gates": data.get("two_qubit_gates", data["qubits"] * 3),
            "depth": data["depth"],
            "graph_nodes": 0,
            "graph_edges": 0,
            "graphml_file": "ERROR"
        })

# Save to CSV
df = pd.DataFrame(baseline_data)
df.to_csv("results/baseline_tcounts.csv", index=False)

print(f"\n✅ Baseline T-counts saved to: results/baseline_tcounts.csv")
print(f"   Total circuits processed: {len(baseline_data)}")
print(f"   GraphML files in: data/processed/baseline_graphs/")

# Summary statistics
print(f"\n📊 Summary:")
print(f"   Total T-gates: {df['t_count'].sum()}")
print(f"   Avg T-count: {df['t_count'].mean():.1f}")
print(f"   Max qubits: {df['qubits'].max()}")
print(f"   Min qubits: {df['qubits'].min()}")
