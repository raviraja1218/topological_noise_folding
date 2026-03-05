import pyzx as zx
import json

print("=" * 60)
print("PyZX 0.9.0 - Final Working Syntax")
print("=" * 60)

# METHOD 1: From QASM
print("\n📄 Loading circuit from QASM...")
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
print("\n🔄 Converting to ZX-diagram...")
g = circuit.to_graph()
print(f"✅ Graph created: {g.num_vertices()} vertices, {g.num_edges()} edges")

# Apply simplification
print("\n🔄 Applying spider fusion...")
zx.simplify.spider_simp(g)
print(f"✅ After simplification: {g.num_vertices()} vertices")

# Save graph - CORRECT METHOD for PyZX 0.9.0
print("\n💾 Saving graph...")

# Method 1: Using PyZX's built-in serializer
import pickle
with open("data/processed/test_graph.pickle", "wb") as f:
    pickle.dump(g, f)
print("✅ Graph saved as pickle: data/processed/test_graph.pickle")

# Method 2: Export as simple JSON (our own format)
graph_data = {
    "num_vertices": g.num_vertices(),
    "num_edges": g.num_edges(),
    "vertices": list(range(g.num_vertices())),
    "edges": [(e[0], e[1]) for e in g.edges()]
}
with open("data/processed/test_graph.json", "w") as f:
    json.dump(graph_data, f, indent=2)
print("✅ Graph saved as JSON: data/processed/test_graph.json")

# Create visualization
print("\n📊 Creating visualization...")
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Draw original circuit
zx.draw(circuit, ax=axes[0])
axes[0].set_title("Original Circuit")

# Draw simplified graph
zx.draw(g, ax=axes[1])
axes[1].set_title("ZX-diagram (simplified)")

plt.tight_layout()
plt.savefig("figures/pyzx_final_test.pdf", dpi=300, bbox_inches='tight')
plt.savefig("figures/pyzx_final_test.png", dpi=300, bbox_inches='tight')
print("✅ Visualization saved: figures/pyzx_final_test.pdf")

# Create success marker
with open("data/processed/pyzx_test_success.txt", "w") as f:
    f.write(f"PyZX test successful on $(date)\n")
    f.write(f"Vertices: {g.num_vertices()}, Edges: {g.num_edges()}\n")

print("\n✅ PyZX test complete - Ready for Phase 2!")
