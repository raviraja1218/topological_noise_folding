import os
from pathlib import Path
import json
import torch

print("=" * 60)
print("PHASE 1 - COMPLETE VERIFICATION")
print("=" * 60)

# Check all required files
required = [
    "data/raw/op_t_mize_manual.json",
    "data/raw/op_t_mize_manual.csv",
    "data/raw/op_t_mize_baseline.pkl",
    "results/baseline_metrics.csv",
    "data/processed/test_graph.pickle",
    "data/processed/test_graph.json",
    "data/processed/pyzx_test_success.txt",
    "figures/pyzx_circuit.png",
    "figures/pyzx_diagram.png",
    "figures/pyzx_comparison.pdf"
]

print("\n📁 Files:")
all_good = True
for f in required:
    if Path(f).exists():
        size = Path(f).stat().st_size
        print(f"  ✅ {f} ({size} bytes)")
    else:
        print(f"  ❌ {f} missing")
        all_good = False

# Check GPU
print(f"\n🎮 GPU: {torch.cuda.get_device_name(0)}")
print(f"   CUDA: {torch.cuda.is_available()}")

# Check dataset
with open("data/raw/op_t_mize_manual.json") as f:
    circuits = json.load(f)
print(f"\n📊 Dataset: {len(circuits)} circuits")
print(f"   Families: {len(set(c['family'] for c in circuits.values()))}")
print(f"   Qubits: {min(c['qubits'] for c in circuits.values())}-{max(c['qubits'] for c in circuits.values())}")

print("\n" + "=" * 60)
if all_good:
    print("✅ PHASE 1 COMPLETED - READY FOR PHASE 2")
else:
    print("❌ PHASE 1 INCOMPLETE")
print("=" * 60)
