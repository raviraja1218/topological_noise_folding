# src/test_zx_conversion_fixed.py
"""
Fixed ZX-conversion test with correct PyZX API
"""
import pyzx as zx
import json
import matplotlib.pyplot as plt

print("=" * 60)
print("ZX-Calculus Conversion Test (Fixed API)")
print("=" * 60)

# Create QASM string
qasm_str = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
h q[0];
cx q[0], q[1];
t q[0];
t q[1];
t q[2];
cx q[1], q[2];
t q[0];
t q[1];
h q[2];
t q[0];
"""

print("\n📄 Creating test QASM circuit...")
with open("data/raw/test_circuit_fixed.qasm", "w") as f:
    f.write(qasm_str)

# Correct PyZX loading method
print("\n🔄 Loading circuit into PyZX...")
# Method 1: From QASM file
circuit = zx.Circuit.from_qasm_file("data/raw/test_circuit_fixed.qasm")
print(f"Circuit loaded with {len(circuit.gates)} gates")

# Alternative Method 2: From string
# circuit = zx.Circuit.from_qasm_str(qasm_str)

# Convert to ZX graph
print("\n🔄 Converting to ZX-diagram...")
g = circuit.to_graph()
print(f"ZX-diagram created: {g.num_vertices()} vertices, {g.num_edges()} edges")

# Apply basic simplification
print("\n🔄 Applying spider fusion...")
zx.simplify.spider_simp(g, quiet=True)
print(f"After spider fusion: {g.num_vertices()} vertices, {g.num_edges()} edges")

# Save the graph
zx.drawer.graph_to_graphml(g, "data/processed/test_circuit_zx_fixed.graphml")

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
zx.draw(circuit, ax=axes[0])
axes[0].set_title("Original Circuit")
zx.draw(g, ax=axes[1])
axes[1].set_title("ZX-diagram (simplified)")
plt.tight_layout()
plt.savefig("figures/test_zx_conversion_fixed.pdf", format='pdf', dpi=300, bbox_inches='tight')
print("✅ Visualization saved to figures/test_zx_conversion_fixed.pdf")

metrics = {
    "original_gates": len(circuit.gates),
    "zx_vertices": g.num_vertices(),
    "zx_edges": g.num_edges()
}
with open("data/processed/test_zx_metrics_fixed.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\n✅ ZX-conversion test complete!")
