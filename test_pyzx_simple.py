import pyzx as zx
print(f"✅ PyZX {zx.__version__} imported successfully")

# Create a simple circuit
circuit = zx.Circuit(3)  # 3 qubit circuit
circuit.add_gate("H", 0)
circuit.add_gate("CX", 1, 0)
circuit.add_gate("T", 2)
print(f"Circuit created with {len(circuit.gates)} gates")

# Convert to graph
g = circuit.to_graph()
print(f"Graph has {g.num_vertices()} vertices")

print("✅ PyZX test passed")
