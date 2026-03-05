# src/generate_baseline_metadata.py
"""
Generate baseline metadata for a small test circuit (5-qubit arithmetic)
to verify the pipeline before scaling up
"""
import json
import time
from pathlib import Path
import numpy as np

# For demonstration, create a simple 5-qubit arithmetic circuit
# In actual implementation, this would load from op-T-mize

def create_test_circuit():
    """Create a 5-qubit test circuit (simplified adder)"""
    circuit = {
        "name": "test_adder_5q",
        "family": "Arithmetic",
        "qubits": 5,
        "gates": [
            # Clifford gates (H, S, CNOT)
            {"type": "H", "qubits": [0]},
            {"type": "H", "qubits": [1]},
            {"type": "CNOT", "qubits": [0, 1]},
            {"type": "S", "qubits": [1]},
            {"type": "CNOT", "qubits": [1, 2]},
            # T gates (non-Clifford)
            {"type": "T", "qubits": [0]},
            {"type": "T", "qubits": [2]},
            {"type": "T", "qubits": [3]},
            {"type": "T", "qubits": [4]},
            {"type": "T", "qubits": [0]},  # Second T on qubit 0
            {"type": "CNOT", "qubits": [2, 3]},
            {"type": "T", "qubits": [1]},
            {"type": "T", "qubits": [2]},
            {"type": "H", "qubits": [4]},
            {"type": "T", "qubits": [3]},
            {"type": "T", "qubits": [4]},
            {"type": "CNOT", "qubits": [0, 4]},
            {"type": "T", "qubits": [0]},
            {"type": "T", "qubits": [1]},
        ],
        "original_metrics": {
            "t_count": 12,  # Count T gates
            "clifford_count": 7,  # H, S, CNOT
            "two_qubit_gates": 4,  # CNOTs
            "depth": 0  # To be computed
        }
    }
    
    # Compute depth (simplified - longest path)
    # This is a placeholder - real depth calculation is more complex
    circuit["original_metrics"]["depth"] = len(circuit["gates"])
    
    return circuit

# Generate metadata for test circuit
print("Generating baseline metadata for test circuit...")
test_circuit = create_test_circuit()

# Save as JSON
with open("data/raw/baseline_test_circuit.json", "w") as f:
    json.dump(test_circuit, f, indent=2)

# Also save as CSV for easy viewing
import pandas as pd
df_gates = pd.DataFrame(test_circuit["gates"])
df_gates.to_csv("data/raw/baseline_test_circuit_gates.csv", index=False)

# Create inventory of all baseline circuits (will be expanded in Phase 2)
baseline_inventory = {
    "test_circuit": test_circuit["name"],
    "test_qubits": test_circuit["qubits"],
    "test_t_count": test_circuit["original_metrics"]["t_count"],
    "total_circuits_planned": 31,
    "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    "note": "Full 31-circuit baseline will be generated in Phase 2"
}

with open("data/raw/baseline_inventory.json", "w") as f:
    json.dump(baseline_inventory, f, indent=2)

print("\n✅ Baseline test metadata generated:")
print("   - data/raw/baseline_test_circuit.json")
print("   - data/raw/baseline_test_circuit_gates.csv")
print("   - data/raw/baseline_inventory.json")
print(f"\nTest circuit: {test_circuit['name']}")
print(f"Qubits: {test_circuit['qubits']}")
print(f"T-count: {test_circuit['original_metrics']['t_count']}")
