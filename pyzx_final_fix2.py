import pyzx as zx
import json
import pickle
import matplotlib.pyplot as plt

print("=" * 60)
print("PyZX 0.9.0 - Final Working Syntax with Drawing")
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
zx.simplify.spider_simp(g, quiet=True)
print(f"✅ After simplification: {g.num_vertices()} vertices")

# Save graph
print("\n💾 Saving graph...")
with open("data/processed/test_graph.pickle", "wb") as f:
    pickle.dump(g, f)
print("✅ Graph saved as pickle: data/processed/test_graph.pickle")

graph_data = {
    "num_vertices": g.num_vertices(),
    "num_edges": g.num_edges(),
    "vertices": list(range(g.num_vertices())),
    "edges": [(e[0], e[1]) for e in g.edges()]
}
with open("data/processed/test_graph.json", "w") as f:
    json.dump(graph_data, f, indent=2)
print("✅ Graph saved as JSON: data/processed/test_graph.json")

# Create visualization - CORRECT SYNTAX for PyZX 0.9.0
print("\n📊 Creating visualization...")

# Method 1: Use PyZX's built-in drawer (saves to file)
print("   Rendering circuit...")
zx.draw(circuit, "figures/pyzx_circuit.png")
print("   ✅ Circuit saved: figures/pyzx_circuit.png")

print("   Rendering ZX-diagram...")
zx.draw(g, "figures/pyzx_diagram.png") 
print("   ✅ Diagram saved: figures/pyzx_diagram.png")

# Method 2: Create side-by-side with matplotlib
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# For matplotlib integration, we need to use draw_matplotlib directly
from pyzx.drawing import draw_matplotlib

# Draw circuit
draw_matplotlib(circuit.to_graph(), ax=axes[0])
axes[0].set_title("Original Circuit")

# Draw simplified graph
draw_matplotlib(g, ax=axes[1])
axes[1].set_title("ZX-diagram (simplified)")

plt.tight_layout()
plt.savefig("figures/pyzx_comparison.pdf", dpi=300, bbox_inches='tight')
plt.savefig("figures/pyzx_comparison.png", dpi=300, bbox_inches='tight')
print("✅ Comparison saved: figures/pyzx_comparison.pdf")

# Create success marker
import datetime
with open("data/processed/pyzx_test_success.txt", "w") as f:
    f.write(f"PyZX test successful on {datetime.datetime.now()}\n")
    f.write(f"Vertices: {g.num_vertices()}, Edges: {g.num_edges()}\n")

print("\n✅ PyZX test complete - Ready for Phase 2!")
