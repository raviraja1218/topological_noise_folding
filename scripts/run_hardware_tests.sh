#!/bin/bash

# Hardware Validation Script
echo "========================================="
echo "🔬 TNF Hardware Validation on IBM Quantum"
echo "========================================="
echo "Token: 4KetLabdZi485z11ggi4xgz0rhoPv2oN7tkQUEFXS8k5"
echo ""

# Activate environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate tnf

# Create results directory
mkdir -p results/hardware

# Check if qiskit is installed
python -c "import qiskit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing Qiskit..."
    pip install qiskit qiskit-ibm-provider
fi

# Run hardware validation
echo ""
echo "Starting hardware validation..."
echo "You will be prompted to choose:"
echo "  1 - Real hardware (may take hours)"
echo "  2 - Simulation (fast)"
echo "  3 - Test connection only"
echo ""

python src/hardware_validation/hardware_results.py

echo ""
echo "✅ Hardware validation script completed"
echo "Check results/hardware/ for output files"
