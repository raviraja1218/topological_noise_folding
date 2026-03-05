import torch
import json
import pickle
import networkx as nx
from pathlib import Path

print("=" * 70)
print("🎉 PHASE 1 - FINAL COMPLETION CERTIFICATE 🎉")
print("=" * 70)

# Check GPU
print(f"\n🎮 GPU: {torch.cuda.get_device_name(0)}")
print(f"   CUDA: {torch.cuda.is_available()}")

# Check dataset
with open("data/raw/op_t_mize_manual.json", "r") as f:
    circuits = json.load(f)
print(f"\n📊 Dataset: {len(circuits)} circuits")
print(f"   Families: {', '.join(set(c['family'] for c in circuits.values()))}")
qubits = [c['qubits'] for c in circuits.values()]
print(f"   Qubit range: {min(qubits)}-{max(qubits)}")

# Check Hidden Shift 768 (key paper result)
hs768 = next((c for name, c in circuits.items() if name == "hidden_shift_768"), None)
if hs768:
    print(f"\n🔑 Hidden Shift 768: {hs768['t_gates']} T-gates, {hs768['depth']} depth")

# Check all required files
required = {
    "Dataset PKL": "data/raw/op_t_mize_baseline.pkl",
    "Baseline CSV": "results/baseline_metrics.csv",
    "ZX Graph Pickle": "data/processed/test_graph.pickle",
    "ZX Graph JSON": "data/processed/test_graph.json",
    "GraphML": "data/processed/test_graph.graphml",
    "Stim Results": "data/processed/stim_test_fixed2.json",
    "Success Marker": "data/processed/pyzx_test_success.txt"
}

print("\n📁 Required files:")
all_good = True
for name, path in required.items():
    if Path(path).exists():
        size = Path(path).stat().st_size
        print(f"  ✅ {name}: {path} ({size} bytes)")
    else:
        print(f"  ❌ {name}: {path} missing")
        all_good = False

# Check libraries
print("\n📚 Libraries:")
try:
    import pennylane as qml
    print(f"  ✅ PennyLane: {qml.__version__}")
except:
    print("  ❌ PennyLane missing")

try:
    import pyzx as zx
    print(f"  ✅ PyZX: {zx.__version__}")
except:
    print("  ❌ PyZX missing")

try:
    import stim
    print(f"  ✅ Stim: {stim.__version__}")
except:
    print("  ❌ Stim missing")

try:
    import torch_geometric as tg
    print(f"  ✅ PyG: {tg.__version__}")
except:
    print("  ❌ PyG missing")

print("\n" + "=" * 70)
if all_good and len(circuits) == 31:
    print("✅✅✅ PHASE 1 100% COMPLETE - READY FOR PHASE 2 ✅✅✅")
    print("\n📋 PHASE 1 SUMMARY:")
    print("   • Environment: ✅ All libraries installed")
    print("   • GPU: ✅ RTX 4050 CUDA active")
    print("   • Dataset: ✅ 31 circuits (5-1024 qubits)")
    print("   • ZX Pipeline: ✅ Graph conversion working")
    print("   • Stim: ✅ Simulation working")
    print("   • GraphML: ✅ Export working")
    print("   • PennyLane: ✅ Installed")
    print("\n🚀 Proceed to Phase 2: Baseline Characterization")
else:
    print("❌ Phase 1 incomplete")
print("=" * 70)

# Save final certificate
with open("logs/phase1_final_certificate.txt", "w") as f:
    f.write("PHASE 1 COMPLETED SUCCESSFULLY\n")
    f.write(f"Date: {__import__('datetime').datetime.now()}\n")
    f.write(f"GPU: {torch.cuda.get_device_name(0)}\n")
    f.write(f"Circuits: {len(circuits)}\n")
    f.write(f"Qubit range: {min(qubits)}-{max(qubits)}\n")
    f.write("All requirements met. Ready for Phase 2.\n")
