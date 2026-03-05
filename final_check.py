import os
from pathlib import Path
import torch
import json

print("=" * 60)
print("PHASE 1 - FINAL CHECK")
print("=" * 60)

# Core requirements (must exist)
core_files = [
    "data/raw/op_t_mize_manual.json",
    "data/raw/op_t_mize_manual.csv",
    "data/raw/op_t_mize_baseline.pkl",
    "results/baseline_metrics.csv",
    "data/processed/test_graph.pickle",
    "data/processed/test_graph.json",
    "data/processed/pyzx_test_success.txt"
]

# Figure files (nice to have)
figures = [
    "figures/pyzx_circuit.png",
    "figures/pyzx_diagram.png"
]

print("\n📁 Core files:")
all_core = True
for f in core_files:
    if Path(f).exists():
        size = Path(f).stat().st_size
        print(f"  ✅ {f} ({size} bytes)")
    else:
        print(f"  ❌ {f} missing")
        all_core = False

print("\n📁 Figures:")
for f in figures:
    if Path(f).exists():
        print(f"  ✅ {f}")
    else:
        print(f"  ⚠️  {f} missing (optional)")

# GPU
print(f"\n🎮 GPU: {torch.cuda.get_device_name(0)}")
print(f"   CUDA: {torch.cuda.is_available()}")

# Dataset
with open("data/raw/op_t_mize_manual.json") as f:
    circuits = json.load(f)
print(f"\n📊 Dataset: {len(circuits)} circuits")
families = set(c['family'] for c in circuits.values())
print(f"   Families: {len(families)} ({', '.join(list(families)[:3])}...)")
qubits = [c['qubits'] for c in circuits.values()]
print(f"   Qubit range: {min(qubits)}-{max(qubits)}")

print("\n" + "=" * 60)
if all_core:
    print("✅ PHASE 1 COMPLETE - READY FOR PHASE 2")
    print("   All core requirements satisfied.")
    
    # Create completion certificate
    with open("logs/phase1_certificate.txt", "w") as f:
        f.write(f"PHASE 1 COMPLETED: {__import__('datetime').datetime.now()}\n")
        f.write(f"GPU: {torch.cuda.get_device_name(0)}\n")
        f.write(f"Circuits: {len(circuits)}\n")
        f.write(f"Qubit range: {min(qubits)}-{max(qubits)}\n")
else:
    print("❌ PHASE 1 INCOMPLETE")
    print("   Missing core files. Run phase1_complete_simple.py")
print("=" * 60)
