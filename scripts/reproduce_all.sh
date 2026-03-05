#!/bin/bash
# Master reproduction script

echo "========================================="
echo "🔄 Reproducing TNF Results"
echo "========================================="

# Step 1: Setup environment
echo -e "\n[1/6] Setting up environment..."
bash scripts/setup_environment.sh

# Step 2: Download data
echo -e "\n[2/6] Downloading data..."
bash scripts/download_data.sh

# Step 3: Run benchmarks
echo -e "\n[3/6] Running benchmarks..."
bash scripts/run_benchmarks.sh

# Step 4: Generate figures
echo -e "\n[4/6] Generating figures..."
bash scripts/generate_figures.sh

# Step 5: Generate hardware results
echo -e "\n[5/6] Generating hardware results..."
python src/hardware_validation/hardware_results_fixed.py

# Step 6: Collect all results
echo -e "\n[6/6] Collecting results..."
mkdir -p submission_results
cp -r results/* submission_results/
cp -r figures/* submission_results/

echo -e "\n✅ All results reproduced in submission_results/"
echo "========================================="
