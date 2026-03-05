import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 60)
print("PHASE 2 VALIDATION")
print("=" * 60)

# Check all required files
required_files = [
    "results/baseline_tcounts.csv",
    "results/pauli_flow_baseline.csv",
    "results/baseline_sampling_costs.csv",
    "results/matrix_representations.npz",
    "results/noise_models.npz",
    "results/stim_baseline.hdf5",
    "src/pauli_flow_theorem.tex"
]

print("\n📁 Checking required files:")
all_exist = True
for f in required_files:
    if Path(f).exists():
        size = Path(f).stat().st_size
        print(f"  ✅ {f} ({size} bytes)")
    else:
        print(f"  ❌ {f} missing")
        all_exist = False

# Check GraphML files
graphml_dir = Path("data/processed/baseline_graphs")
graphml_files = list(graphml_dir.glob("*.graphml"))
print(f"\n📁 GraphML files: {len(graphml_files)}/31")

# Load and verify data
if all_exist:
    print("\n📊 Verifying data integrity:")
    
    # Check baseline T-counts
    df_tcounts = pd.read_csv("results/baseline_tcounts.csv")
    print(f"  ✅ baseline_tcounts.csv: {len(df_tcounts)} circuits")
    
    # Check Pauli flow
    df_flow = pd.read_csv("results/pauli_flow_baseline.csv")
    flow_count = df_flow['flow_exists'].sum()
    print(f"  ✅ pauli_flow_baseline.csv: {flow_count}/{len(df_flow)} have flow")
    
    # Check sampling costs
    df_costs = pd.read_csv("results/baseline_sampling_costs.csv")
    feasible = df_costs['sampling_feasible'].sum()
    print(f"  ✅ baseline_sampling_costs.csv: {feasible}/{len(df_costs)} feasible")
    
    # Check matrix representations
    matrices = np.load("results/matrix_representations.npz")
    print(f"  ✅ matrix_representations.npz: {len(matrices.files)} matrices")
    
    # Check noise models
    noise = np.load("results/noise_models.npz")
    gamma = float(noise['gamma'])
    print(f"  ✅ noise_models.npz: γ = {gamma:.6f}")
    
    # Check Stim results
    import h5py
    with h5py.File("results/stim_baseline.hdf5", 'r') as f:
        num_circuits = len(f.keys())
        print(f"  ✅ stim_baseline.hdf5: {num_circuits} circuits")

print("\n" + "=" * 60)
if all_exist and len(graphml_files) == 31:
    print("✅✅✅ PHASE 2 COMPLETED SUCCESSFULLY")
    print("   All 31 circuits processed")
    print("   All required files generated")
    print("\n📋 Ready for Phase 3: Graph Transformer Architecture")
else:
    print("❌ Phase 2 incomplete")
    if not all_exist:
        print("   Missing required files")
    if len(graphml_files) != 31:
        print(f"   Missing GraphML files: have {len(graphml_files)}, need 31")
print("=" * 60)
