import pyzx as zx
import json
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import os

print("=" * 60)
print("PHASE 1 - COMPLETION SCRIPT")
print("=" * 60)

# Create directories
os.makedirs("figures", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# Load circuit
print("\n📄 Creating test circuit...")
qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0], q[1];
t q[0];
t q[1];
"""
circuit = zx.Circuit.from_qasm(qasm)
print(f"✅ Circuit loaded with {len(circuit.gates)} gates")

# Convert to graph
g = circuit.to_graph()
print(f"✅ Graph: {g.num_vertices()} vertices")

# Simplify
zx.simplify.spider_simp(g, quiet=True)
print(f"✅ Simplified: {g.num_vertices()} vertices")

# Save graph
with open("data/processed/test_graph.pickle", "wb") as f:
    pickle.dump(g, f)
print("✅ Graph saved")

# Save simple JSON
simple_data = {
    "vertices": g.num_vertices(),
    "edges": g.num_edges()
}
with open("data/processed/test_graph.json", "w") as f:
    json.dump(simple_data, f)

# Create individual figures (SIMPLE APPROACH - works every time)
print("\n📊 Creating figures...")

# Figure 1: Circuit only
plt.figure(figsize=(6,4))
zx.draw(circuit)
plt.title("Original Circuit")
plt.savefig("figures/pyzx_circuit.png", dpi=300, bbox_inches='tight')
plt.savefig("figures/pyzx_circuit.pdf", dpi=300, bbox_inches='tight')
plt.close()
print("✅ Circuit figure saved")

# Figure 2: ZX diagram only
plt.figure(figsize=(6,4))
zx.draw(g)
plt.title("ZX Diagram")
plt.savefig("figures/pyzx_diagram.png", dpi=300, bbox_inches='tight')
plt.savefig("figures/pyzx_diagram.pdf", dpi=300, bbox_inches='tight')
plt.close()
print("✅ ZX diagram saved")

# Success marker
with open("data/processed/pyzx_test_success.txt", "w") as f:
    f.write(f"Phase 1 completed: {datetime.datetime.now()}\n")
    f.write(f"Vertices: {g.num_vertices()}, Edges: {g.num_edges()}\n")

print("\n✅ PHASE 1 COMPLETED SUCCESSFULLY")
print("   Files created:")
print("   - data/processed/test_graph.pickle")
print("   - data/processed/test_graph.json")
print("   - data/processed/pyzx_test_success.txt")
print("   - figures/pyzx_circuit.png/pdf")
print("   - figures/pyzx_diagram.png/pdf")
