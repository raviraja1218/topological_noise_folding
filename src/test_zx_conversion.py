# src/test_zx_conversion.py
"""
Test PyZX by converting a small circuit to ZX-diagram
"""
import pyzx as zx
import json
import matplotlib.pyplot as plt

# Load test circuit metadata
with open("data/raw/baseline_test_circuit.json", "r") as f:
    circuit_data = json.load(f)

print("=" * 60)
print("ZX-Calculus Conversion Test")
print("=" * 60)

# Create a simple circuit manually (since we don't have actual QASM yet)
# This is a Bell state preparation + T gates for demonstration
def create_test_qasm():
    """Create a simple QASM circuit for testing"""
    qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[3];
    // Clifford part
    h q[0];
    cx q[0], q[1];
    // T gates
    t q[0];
    t q[1];
    t q[2];
    cx q[1], q[2];
    t q[0];
    t q[1];
    h q[2];
    t q[0];
    """
    return qasm

print("\n📄 Creating test QASM circuit...")
qasm_str = create_test_qasm()

# Save QASM for reference
with open("data/raw/test_circuit.qasm", "w") as f:
    f.write(qasm_str)

# Load circuit into PyZX
print("\n🔄 Loading circuit into PyZX...")
circuit = zx.Circuit.load(qasm_str, 'qasm')
print(f"Circuit loaded: {circuit.name if hasattr(circuit, 'name') else 'unnamed'}")
print(f"Gates: {len(circuit.gates)}")

# Convert to ZX graph
print("\n🔄 Converting to ZX-diagram...")
g = circuit.to_graph()
print(f"ZX-diagram created: {g.num_vertices()} vertices, {g.num_edges()} edges")

# Apply basic simplification
print("\n🔄 Applying spider fusion (basic simplification)...")
zx.simplify.spider_simp(g, quiet=True)
print(f"After spider fusion: {g.num_vertices()} vertices, {g.num_edges()} edges")

# Save the graph in GraphML format (for Phase 2)
print("\n💾 Saving ZX-diagram...")
zx.drawer.graph_to_graphml(g, "data/processed/test_circuit_zx.graphml")

# Create visualization
print("\n📊 Generating visualization...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Original circuit
zx.draw(circuit, ax=axes[0])
axes[0].set_title("Original Circuit")

# Simplified ZX-diagram
zx.draw(g, ax=axes[1])
axes[1].set_title("ZX-diagram (after spider fusion)")

plt.tight_layout()
plt.savefig("figures/test_zx_conversion.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig("figures/test_zx_conversion.png", dpi=300, bbox_inches='tight')
print("   - figures/test_zx_conversion.pdf")
print("   - figures/test_zx_conversion.png")

# Extract metrics
metrics = {
    "original_gates": len(circuit.gates),
    "zx_vertices": g.num_vertices(),
    "zx_edges": g.num_edges(),
    "simplified_vertices": g.num_vertices(),
    "simplified_edges": g.num_edges()
}

with open("data/processed/test_zx_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\n✅ ZX-conversion test complete!")
print(f"Metrics saved to: data/processed/test_zx_metrics.json")
