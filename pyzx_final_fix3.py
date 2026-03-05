import pyzx as zx
import json
import pickle
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (prevents window popup)
import matplotlib.pyplot as plt
import datetime
import os

print("=" * 60)
print("PyZX 0.9.0 - Final Working Syntax (No GUI)")
print("=" * 60)

# Create figures directory if it doesn't exist
os.makedirs("figures", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

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

# Create simple graph data JSON
graph_data = {
    "num_vertices": g.num_vertices(),
    "num_edges": g.num_edges(),
    "vertices": list(range(g.num_vertices())),
    "edges": [(int(e[0]), int(e[1])) for e in g.edges()]
}
with open("data/processed/test_graph.json", "w") as f:
    json.dump(graph_data, f, indent=2)
print("✅ Graph saved as JSON: data/processed/test_graph.json")

# METHOD 1: PyZX's built-in PNG export (works reliably)
print("\n📊 Creating visualizations (Method 1 - PyZX built-in)...")
zx.draw(circuit, "figures/pyzx_circuit.png")
print("   ✅ Circuit saved: figures/pyzx_circuit.png")

zx.draw(g, "figures/pyzx_diagram.png")
print("   ✅ Diagram saved: figures/pyzx_diagram.png")

# METHOD 2: Create matplotlib figure without showing it
print("\n📊 Creating visualizations (Method 2 - Matplotlib)...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# For PyZX 0.9.0, draw_matplotlib doesn't take ax parameter
# Instead, get the figure from PyZX and combine
from pyzx.drawing import draw_matplotlib

# Draw circuit
draw_matplotlib(circuit.to_graph())
plt.gca().set_title("Original Circuit")
plt.savefig("figures/pyzx_circuit_matplotlib.png", dpi=300, bbox_inches='tight')
plt.close()

# Draw simplified graph
draw_matplotlib(g)
plt.gca().set_title("ZX-diagram (simplified)")
plt.savefig("figures/pyzx_diagram_matplotlib.png", dpi=300, bbox_inches='tight')
plt.close()

print("   ✅ Matplotlib versions saved")

# Create a combined image manually
fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# Recreate both in same figure
draw_matplotlib(circuit.to_graph())
ax1 = plt.gca()
ax1.set_title("Original Circuit")
ax1.figure = fig
fig.add_axes(ax1)

plt.figure()  # New figure
draw_matplotlib(g)
ax2 = plt.gca()
ax2.set_title("ZX-diagram (simplified)")
ax2.figure = fig
fig.add_axes(ax2)

plt.tight_layout()
plt.savefig("figures/pyzx_comparison.pdf", dpi=300, bbox_inches='tight')
plt.savefig("figures/pyzx_comparison.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Comparison saved: figures/pyzx_comparison.pdf")

# Create success marker
with open("data/processed/pyzx_test_success.txt", "w") as f:
    f.write(f"PyZX test successful on {datetime.datetime.now()}\n")
    f.write(f"Vertices: {g.num_vertices()}, Edges: {g.num_edges()}\n")

print("\n✅ PyZX test complete - All files created!")
print("   Check figures/ directory for PNG and PDF outputs")
