import numpy as np
import json
from pathlib import Path

print("=" * 60)
print("STEP 2.3: Baseline Noise Model Implementation")
print("=" * 60)

# Depolarizing noise parameters
p = 0.001  # Standard benchmark error rate
print(f"\n📊 Noise model: Depolarizing channel")
print(f"   Error rate p = {p} per gate")

# Single-qubit Pauli transfer matrix for depolarizing noise
# Basis order: I, X, Y, Z
ptm_single = np.diag([1, 1-p, 1-p, 1-p])
print(f"\n✅ Single-qubit PTM shape: {ptm_single.shape}")

# Two-qubit PTM (Kronecker product)
ptm_two = np.kron(ptm_single, ptm_single)
print(f"✅ Two-qubit PTM shape: {ptm_two.shape}")

# Compute gamma factor for PEC
gamma = 1 / (1 - (4/3) * p)
print(f"\n📈 Gamma factor γ = {gamma:.6f}")
print(f"   PEC sampling cost: C = γ^(2K) where K = number of gates")

# Save noise models
npz_path = "results/noise_models.npz"
np.savez(npz_path,
         p=p,
         ptm_single_qubit=ptm_single,
         ptm_two_qubit=ptm_two,
         gamma=gamma)

# Save description as JSON
description = {
    "noise_model": "depolarizing",
    "error_rate": p,
    "gamma": gamma,
    "basis": ["I", "X", "Y", "Z"],
    "reference": "Standard benchmark for quantum error mitigation",
    "date": "2026-02-25"
}

with open("results/noise_model_description.json", "w") as f:
    json.dump(description, f, indent=2)

print(f"\n✅ Noise models saved to: {npz_path}")
print(f"✅ Description saved to: results/noise_model_description.json")

# Quick verification
print(f"\n🔍 Verification:")
print(f"   PTM single-qubit diagonal: {np.diag(ptm_single)}")
print(f"   PTM two-qubit trace: {np.trace(ptm_two):.2f}")
print(f"   Gamma matches theory: {abs(gamma - 1.00133) < 1e-5}")
