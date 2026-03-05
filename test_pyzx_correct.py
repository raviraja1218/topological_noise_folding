import pyzx as zx
print(f"✅ PyZX {zx.__version__}")

# Method 1: Create from QASM string (RECOMMENDED)
qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0], q[1];
t q[0];
t q[1];
"""

print("\nMethod 1: Load from QASM string")
circuit = zx.Circuit.from_qasm_str(qasm)
print(f"✅ Circuit loaded with {len(circuit.gates)} gates")

# Convert to graph
g = circuit.to_graph()
print(f"✅ Graph has {g.num_vertices()} vertices, {g.num_edges()} edges")
print("✅ PyZX graph conversion SUCCESSFUL")

# Save graph info
with open("data/processed/pyzx_test_success.txt", "w") as f:
    f.write(f"Vertices: {g.num_vertices()}, Edges: {g.num_edges()}")
