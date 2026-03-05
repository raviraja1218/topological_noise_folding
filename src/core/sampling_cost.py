import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 60)
print("STEP 2.4: Baseline Sampling Cost Calculation")
print("=" * 60)

# Load baseline T-counts
tcounts_path = "results/baseline_tcounts.csv"
if not Path(tcounts_path).exists():
    print(f"❌ {tcounts_path} not found. Run baseline_analysis.py first.")
    exit(1)

df = pd.read_csv(tcounts_path)
print(f"\n📂 Loaded {len(df)} circuits from {tcounts_path}")

# Load noise model
try:
    noise_data = np.load("results/noise_models.npz")
    gamma = float(noise_data['gamma'])
    p = float(noise_data['p'])
    print(f"✅ Loaded noise model: γ = {gamma:.6f}, p = {p}")
except:
    # Fallback to theoretical
    p = 0.001
    gamma = 1 / (1 - (4/3) * p)
    print(f"⚠️ Using theoretical γ = {gamma:.6f}")

# Calculate sampling costs for multiple depths
results = []

for _, row in df.iterrows():
    circuit_name = row['circuit_name']
    qubits = row['qubits']
    K = row['t_count']  # Number of noisy gates
    
    # Calculate costs at different depths
    C_original = gamma ** (2 * K)
    C_half = gamma ** (2 * K/2)
    C_quarter = gamma ** (2 * K/4)
    C_double = gamma ** (4 * K)
    
    # Log10 for easier reading
    log10_original = np.log10(C_original) if C_original < 1e308 else float('inf')
    
    results.append({
        "circuit_name": circuit_name,
        "family": row['family'],
        "qubits": qubits,
        "gates_K": K,
        "gamma": gamma,
        "C_original": C_original,
        "C_half": C_half,
        "C_quarter": C_quarter,
        "C_double": C_double,
        "log10_C_original": log10_original,
        "sampling_feasible": log10_original < 12  # 10^12 samples practical limit
    })

# Save to CSV
results_df = pd.DataFrame(results)
output_path = "results/baseline_sampling_costs.csv"
results_df.to_csv(output_path, index=False)
print(f"\n✅ Sampling costs saved to: {output_path}")

# Summary statistics
print(f"\n📊 Summary:")
feasible = results_df['sampling_feasible'].sum()
print(f"   Circuits feasible (log10 C < 12): {feasible}/{len(results_df)}")

# Show exponential wall
print(f"\n📈 Exponential wall examples:")
large_circuits = results_df.nlargest(5, 'log10_C_original')
for _, row in large_circuits.iterrows():
    print(f"   {row['circuit_name']}: log10 C = {row['log10_C_original']:.1f}")

# Save for Figure 2
fig2_data = results_df[['circuit_name', 'qubits', 'gates_K', 'log10_C_original']].copy()
fig2_data.to_csv("results/figure2_baseline_surface.csv", index=False)
print(f"\n✅ Figure 2 baseline data saved to: results/figure2_baseline_surface.csv")
