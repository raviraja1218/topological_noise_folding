# src/verify_imports.py
import sys
print(f"Python version: {sys.version}")

# Core ML
import torch
import torch_geometric
print(f"PyTorch Geometric: {torch_geometric.__version__}")

# Quantum
import pyzx
import stim
import pennylane as qml
print(f"PyZX version: {pyzx.__version__}")
print(f"Stim version: {stim.__version__}")
print(f"PennyLane version: {qml.__version__}")

# Scientific
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")

# Visualization
import manim
print(f"Manim version: {manim.__version__}")

print("\n✅ All imports successful!")
