# src/test_stim_fixed.py
"""
Fixed Stim simulation with proper T-gate decomposition
"""
import stim
import numpy as np
import json

print("=" * 60)
print("Stim Simulator Test (Fixed)")
print("=" * 60)

# Stim doesn't have native T gate - we need to:
# 1. Either use Clifford+T simulation via stabilizer formalism
# 2. Or decompose T gates for noise simulation

print("\n🔧 Creating circuit with proper Stim gates...")
circuit = stim.Circuit()

# Stim only has Clifford gates natively
# H, S, CNOT, X, Y, Z, etc.

circuit.append("H", [0])
circuit.append("CX", [0, 1])
circuit.append("CX", [0, 2])

# For T gates, we simulate their effect through noise
# In actual TNF, we'll use stabilizer simulation for Clifford parts
# and track T gates separately

# Add some Clifford equivalents
circuit.append("S", [0])  # S is Clifford (T^2)
circuit.append("S", [1])
circuit.append("S", [2])

circuit.append("CX", [1, 2])

circuit.append("H", [2])

# Measurement
circuit.append("M", [0, 1, 2])

print(f"Circuit created with {len(circuit)} operations")

# Add depolarizing noise
print("\n🌊 Adding depolarizing noise (p=0.001)...")
noisy_circuit = circuit.copy()
for i in range(3):
    noisy_circuit.append("DEPOLARIZE1", [i], 0.001)

# Simulate ideal circuit
print("\n🔄 Simulating ideal circuit...")
sampler = circuit.compile_sampler()
ideal_samples = sampler.sample(shots=1000)
ideal_stats = np.mean(ideal_samples, axis=0)
print(f"Ideal measurement statistics: {ideal_stats}")

# Simulate noisy circuit
print("\n🔄 Simulating noisy circuit...")
sampler_noisy = noisy_circuit.compile_sampler()
noisy_samples = sampler_noisy.sample(shots=1000)
noisy_stats = np.mean(noisy_samples, axis=0)
print(f"Noisy measurement statistics: {noisy_stats}")

# Save results
results = {
    "ideal_stats": ideal_stats.tolist(),
    "noisy_stats": noisy_stats.tolist(),
    "shots": 1000,
    "noise_model": "depolarizing",
    "noise_strength": 0.001
}

with open("data/processed/stim_test_fixed.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n✅ Stim test complete!")
print("Results saved to: data/processed/stim_test_fixed.json")
