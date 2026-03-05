#!/bin/bash
# Generate all paper figures

echo "📈 Generating figures..."

# Activate environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate tnf

# Run figure generation scripts
python src/analyze_loss.py
python src/plot_paper_training.py
python src/figures/fig3_benchmarks.py

echo "✅ Figures generated"
