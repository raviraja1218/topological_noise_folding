import sys
print(f"Python version: {sys.version}")

# Core ML
import torch
import torch_geometric
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"PyTorch Geometric: {torch_geometric.__version__}")

# Quantum - Skip PennyLane if not available
try:
    import pyzx
    print(f"PyZX version: {pyzx.__version__}")
except ImportError as e:
    print(f"PyZX import failed: {e}")

try:
    import stim
    print(f"Stim version: {stim.__version__}")
except ImportError as e:
    print(f"Stim import failed: {e}")

# Try PennyLane but don't fail if missing
try:
    import pennylane as qml
    print(f"PennyLane version: {qml.__version__}")
except ImportError as e:
    print(f"PennyLane import failed: {e} (continuing without it)")

# Scientific
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")

# Try SciencePlots
try:
    import scienceplots
    print("SciencePlots: Available")
except ImportError:
    print("SciencePlots: Not installed")

print("\n✅ Verification complete!")
