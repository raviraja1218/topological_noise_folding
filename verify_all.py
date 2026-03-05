import sys
print(f"Python: {sys.version}")

try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}")
except: print("❌ PyTorch missing")

try:
    import pyzx
    print(f"✅ PyZX: {pyzx.__version__}")
except: print("❌ PyZX missing")

try:
    import stim
    print(f"✅ Stim: {stim.__version__}")
except: print("❌ Stim missing")

try:
    import torch_geometric
    print(f"✅ PyG: {torch_geometric.__version__}")
except: print("❌ PyG missing")

try:
    import numpy as np
    print(f"✅ NumPy: {np.__version__}")
except: print("❌ NumPy missing")

try:
    import pandas as pd
    print(f"✅ Pandas: {pd.__version__}")
except: print("❌ Pandas missing")

try:
    import pkg_resources
    print("✅ pkg_resources working")
except: print("❌ pkg_resources missing")

print("\n✅ Verification complete")
