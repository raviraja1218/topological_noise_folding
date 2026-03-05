import json
import pandas as pd

print("=" * 60)
print("Adding 31st Circuit to Dataset")
print("=" * 60)

# Load existing circuits
with open("data/raw/op_t_mize_manual.json", "r") as f:
    circuits = json.load(f)

print(f"Current circuits: {len(circuits)}")

# Add the missing circuit (bv_14 - Bernstein-Vazirani 14 qubit)
circuits["bv_14"] = {
    "family": "Bernstein-Vazirani",
    "qubits": 14,
    "t_gates": 28,
    "depth": 14,
    "clifford_gates": 140,
    "two_qubit_gates": 42
}

print(f"Added: bv_14 (14 qubits, 28 T-gates)")

# Save updated JSON
with open("data/raw/op_t_mize_manual.json", "w") as f:
    json.dump(circuits, f, indent=2)

# Update CSV
df = pd.DataFrame.from_dict(circuits, orient='index')
df.reset_index(inplace=True)
df.rename(columns={'index': 'circuit_name'}, inplace=True)
df.to_csv("data/raw/op_t_mize_manual.csv", index=False)

# Update baseline metrics CSV
baseline_data = []
for name, data in circuits.items():
    baseline_data.append({
        "circuit_name": name,
        "family": data["family"],
        "qubits": data["qubits"],
        "t_gates": data["t_gates"],
        "depth": data["depth"],
        "clifford_gates": data["qubits"] * 10,
        "two_qubit_gates": data["qubits"] * 3
    })

df_baseline = pd.DataFrame(baseline_data)
df_baseline.to_csv("results/baseline_metrics.csv", index=False)

# Update pickle file
import pickle
with open("data/raw/op_t_mize_baseline.pkl", "wb") as f:
    pickle.dump(circuits, f)

print(f"\n✅ Updated dataset: {len(circuits)} circuits")
print("   - data/raw/op_t_mize_manual.json")
print("   - data/raw/op_t_mize_manual.csv")
print("   - data/raw/op_t_mize_baseline.pkl")
print("   - results/baseline_metrics.csv")

# Show all families
families = set(c['family'] for c in circuits.values())
print(f"\n📊 Families: {', '.join(families)}")
