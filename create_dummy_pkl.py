import pickle
import json

# Create a simple pickle file (for compatibility)
with open("data/raw/op_t_mize_manual.json", "r") as f:
    circuits = json.load(f)

with open("data/raw/op_t_mize_baseline.pkl", "wb") as f:
    pickle.dump(circuits, f)

print("✅ data/raw/op_t_mize_baseline.pkl created")
