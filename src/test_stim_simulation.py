# src/test_stim_simulation.py
"""
Test Stim by simulating a simple circuit with noise
"""
import stim
import numpy as np
import json

print("=" * 60)
print("Stim Simulator Test")
print("=" * 60)

# Create a simple 3-qubit GHZ state circuit with T gates
print("\n🔧 Creating GHZ + T circuit...")
circuit = stim.Circuit()
circuit.append("H", [0])
circuit.append("CX", [0, 1])
circuit.append("CX", [0, 2])
# Add some T gates
circuit.append("T", [0])
circuit.append("T", [1])
circuit.append("T", [2])
circuit.append("CX", [1, 2])
circuit.append("T", [0])
circuit.append("T", [1])
circuit.append("H", [2])
# Measurement
circuit.append("M", [0, 1, 2])

print(f"Circuit created with {len(circuit)} operations")

# Add noise (depolarizing channel after each operation)
print("\n🌊 Adding depolarizing noise (p=0.001)...")
noisy_circuit = circuit.copy()
noisy_circuit.append("DEPOLARIZE1", [0, 1, 2], 0.001)

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

# Extract error rates
error_rate = np.mean(np.abs(ideal_stats - noisy_stats))
print(f"\n📊 Average error rate: {error_rate:.4f}")

# Save results
results = {
    "ideal_stats": ideal_stats.tolist(),
    "noisy_stats": noisy_stats.tolist(),
    "error_rate": float(error_rate),
    "shots": 1000,
    "noise_model": "depolarizing",
    "noise_strength": 0.001
}

with open("data/processed/stim_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n✅ Stim test complete!")
print("Results saved to: data/processed/stim_test_results.json")

# Compute gamma for PEC (simplified)
p = 0.001
gamma = 1 / (1 - (4/3)*p)
print(f"\n📈 Depolarizing noise γ factor: {gamma:.6f}")
print(f"    For a circuit with K gates, sampling cost ∝ γ^(2K)")
