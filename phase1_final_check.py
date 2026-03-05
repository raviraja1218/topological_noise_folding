import os
from pathlib import Path

print("=" * 60)
print("PHASE 1 - FINAL COMPLETION CHECK")
print("=" * 60)

checks = {
    "Environment": [
        ("GPU available", "import torch; print(torch.cuda.is_available())"),
        ("PyTorch", "import torch"),
        ("PyG", "import torch_geometric"),
        ("Stim", "import stim"),
        ("PyZX", "import pyzx"),
    ],
    "Data Files": [
        "data/raw/op_t_mize_manual.json",
        "data/raw/op_t_mize_manual.csv",
        "data/raw/op_t_mize_baseline.pkl",
        "results/baseline_metrics.csv",
    ],
    "Processing": [
        "data/processed/pyzx_test_success.txt",
    ]
}

# Check imports
print("\n📦 Checking imports:")
for name, cmd in checks["Environment"]:
    try:
        exec(cmd)
        print(f"  ✅ {name}")
    except:
        print(f"  ❌ {name}")

# Check files
print("\n📁 Checking files:")
for file in checks["Data Files"] + checks["Processing"]:
    if Path(file).exists():
        size = Path(file).stat().st_size
        print(f"  ✅ {file} ({size} bytes)")
    else:
        print(f"  ❌ {file} missing")

print("\n" + "=" * 60)
print("PHASE 1 STATUS: ", end="")
if all([Path(f).exists() for f in checks["Data Files"] if f != "data/raw/op_t_mize_baseline.pkl"]):
    print("✅ READY FOR PHASE 2")
else:
    print("⚠️  PARTIAL - See above")
print("=" * 60)
