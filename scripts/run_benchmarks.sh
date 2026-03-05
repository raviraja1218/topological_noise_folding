#!/bin/bash
# Run all benchmarks

echo "📊 Running benchmarks..."

# Activate environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate tnf

# Run benchmark expansion
python src/benchmarks/run_full_benchmark.py

# Run ablation study
python src/ablation/run_ablation.py

echo "✅ Benchmarks complete"
