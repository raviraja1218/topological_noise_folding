import pandas as pd
import json

# Load manual circuits
with open("data/raw/op_t_mize_manual.json", "r") as f:
    circuits = json.load(f)

# Create baseline metrics
baseline_data = []
for name, data in circuits.items():
    baseline_data.append({
        "circuit_name": name,
        "family": data["family"],
        "qubits": data["qubits"],
        "t_gates": data["t_gates"],
        "depth": data["depth"],
        "clifford_gates": data["qubits"] * 10,  # Approximate
        "two_qubit_gates": data["qubits"] * 3    # Approximate
    })

df = pd.DataFrame(baseline_data)
df.to_csv("results/baseline_metrics.csv", index=False)
print("✅ results/baseline_metrics.csv created")
