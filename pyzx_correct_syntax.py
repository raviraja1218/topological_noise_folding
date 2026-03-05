import pyzx as zx

print("=" * 60)
print("PyZX 0.9.0 Correct Syntax")
print("=" * 60)

# METHOD 1: From QASM string (CORRECT)
print("\n📄 Method 1: from_qasm()")
qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0], q[1];
t q[0];
t q[1];
"""
circuit = zx.Circuit.from_qasm(qasm)  # NOT from_qasm_str
print(f"✅ Circuit loaded with {len(circuit.gates)} gates")

# METHOD 2: Building gates manually
print("\n🔧 Method 2: Manual gate addition")
c = zx.Circuit(2)
c.add_gate("H", 0)
c.add_gate("CNOT", 0, 1)  # Use "CNOT" not "CX"
c.add_gate("T", 0)
c.add_gate("T", 1)
print(f"✅ Circuit built with {len(c.gates)} gates")

# Convert to graph
g = circuit.to_graph()
print(f"\n📊 ZX-diagram: {g.num_vertices()} vertices, {g.num_edges()} edges")

# Apply simplification
zx.simplify.spider_simp(g)
print(f"✅ After spider fusion: {g.num_vertices()} vertices")

# Save graph
zx.graph_to_graphml(g, "data/processed/test_graph.graphml")
print("✅ Graph saved to data/processed/test_graph.graphml")

# Create visualization (optional)
try:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    zx.draw(g, ax=ax)
    plt.savefig("figures/test_graph.pdf", dpi=300, bbox_inches='tight')
    print("✅ Visualization saved to figures/test_graph.pdf")
except:
    print("⚠️ Visualization skipped")

print("\n✅ PyZX syntax test complete - Ready for Phase 2!")
