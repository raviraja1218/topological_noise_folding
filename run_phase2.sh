#!/bin/bash

echo "=========================================================="
echo "PHASE 2 EXECUTION - TOPOLOGICAL NOISE FOLDING"
echo "=========================================================="
echo

# Step 2.1: Baseline Circuit Analysis
echo "Running Step 2.1: baseline_analysis.py"
python src/baseline_analysis.py
echo
read -p "Press Enter to continue to Step 2.2..."

# Step 2.2: Pauli Flow Matrix Implementation
echo "Running Step 2.2: pauli_flow_core.py"
python src/pauli_flow_core.py
echo
read -p "Press Enter to continue to Step 2.3..."

# Step 2.3: Noise Model Implementation
echo "Running Step 2.3: noise_models.py"
python src/noise_models.py
echo
read -p "Press Enter to continue to Step 2.4..."

# Step 2.4: Sampling Cost Calculation
echo "Running Step 2.4: sampling_cost.py"
python src/sampling_cost.py
echo
read -p "Press Enter to continue to Step 2.5..."

# Step 2.5: Stabilizer Simulation
echo "Running Step 2.5: stim_baseline.py"
python src/stim_baseline.py
echo
read -p "Press Enter for validation..."

# Step 2.6: Validation
echo "Running Step 2.6: validate_phase2.py"
python src/validate_phase2.py

echo
echo "=========================================================="
echo "PHASE 2 EXECUTION COMPLETE"
echo "=========================================================="
