import os
import torch
import pyzx
import stim
import numpy as np
import pandas as pd
from pathlib import Path

print("=" * 60)
print("PHASE 1 COMPLETION VERIFICATION")
print("=" * 60)

checks = []

# GPU
gpu_ok = torch.cuda.is_available()
print(f"✅ GPU: {gpu_ok} - {torch.cuda.get_device_name(0) if gpu_ok else 'None'}")
checks.append(gpu_ok)

# PyZX
try:
    print(f"✅ PyZX: {pyzx.__version__}")
    checks.append(True)
except:
    print("❌ PyZX failed")
    checks.append(False)

# Stim
try:
    print(f"✅ Stim: {stim.__version__}")
    checks.append(True)
except:
    print("❌ Stim failed")
    checks.append(False)

# Data files
data_files = [
    "data/raw/op_t_mize_manual.json",
    "data/raw/op_t_mize_manual.csv"
]

for file in data_files:
    if Path(file).exists():
        print(f"✅ {file}")
        checks.append(True)
    else:
        print(f"❌ {file} missing")
        checks.append(False)

# Summary
if all(checks):
    print("\n✅ PHASE 1 COMPLETED - READY FOR PHASE 2")
else:
    print(f"\n❌ PHASE 1 INCOMPLETE - {checks.count(False)} checks failed")
