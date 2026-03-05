import pyzx as zx

# List available gate types
print("Available gate types in PyZX 0.9.0:")
from pyzx.circuit import gate_types
for gate_name in list(gate_types.keys())[:20]:  # Show first 20
    print(f"  - {gate_name}")

# Try different CX variations
print("\nTrying different CX syntax:")

# Method 1: From QASM (always works)
qasm = "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncx q[0], q[1];"
circuit = zx.Circuit.from_qasm_str(qasm)
print("✅ Method 1 (QASM) works")

# Method 2: Using "CNOT" instead of "CX"
try:
    circuit2 = zx.Circuit(2)
    circuit2.add_gate("CNOT", 0, 1)
    print("✅ Method 2 (CNOT) works")
except Exception as e:
    print(f"❌ Method 2 failed: {e}")

# Method 3: Using lowercase
try:
    circuit3 = zx.Circuit(2)
    circuit3.add_gate("cx", 0, 1)
    print("✅ Method 3 (lowercase) works")
except Exception as e:
    print(f"❌ Method 3 failed: {e}")
