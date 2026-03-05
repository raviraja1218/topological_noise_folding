import stim
print(f"✅ Stim {stim.__version__} imported successfully")

circuit = stim.Circuit()
circuit.append("H", [0])
circuit.append("CX", [0, 1])
circuit.append("M", [0, 1])

sampler = circuit.compile_sampler()
samples = sampler.sample(shots=10)
print(f"Sampled {len(samples)} shots")
print("✅ Stim test passed")
