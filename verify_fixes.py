import json
import pickle
from pathlib import Path

print("=" * 60)
print("VERIFYING MISSING ITEMS FIXES")
print("=" * 60)

# Check 1: PennyLane
try:
    import pennylane as qml
    print(f"✅ PennyLane {qml.__version__} installed")
except ImportError:
    print("❌ PennyLane still missing")

# Check 2: 31 circuits
with open("data/raw/op_t_mize_manual.json", "r") as f:
    circuits = json.load(f)
print(f"✅ Circuits: {len(circuits)} (should be 31)")

# Check 3: GraphML
graphml_files = list(Path("data/processed").glob("*.graphml"))
if graphml_files:
    for f in graphml_files:
        size = f.stat().st_size
        print(f"✅ GraphML: {f.name} ({size} bytes)")
else:
    print("❌ No GraphML files found")

# Check 4: All required files
required = [
    "data/raw/op_t_mize_baseline.pkl",
    "results/baseline_metrics.csv"
]

print("\n📁 Required files:")
for f in required:
    if Path(f).exists():
        size = Path(f).stat().st_size
        print(f"  ✅ {f} ({size} bytes)")
    else:
        print(f"  ❌ {f} missing")

print("\n" + "=" * 60)
if len(circuits) == 31 and all(Path(f).exists() for f in required):
    print("✅ ALL MISSING ITEMS FIXED - Ready for Phase 2")
else:
    print("⚠️ Some fixes still needed")
print("=" * 60)
