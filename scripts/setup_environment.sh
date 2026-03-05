#!/bin/bash
# Setup conda environment

echo "🔧 Setting up environment..."

# Create conda environment
conda create -n tnf python=3.10 -y

# Activate
source $(conda info --base)/etc/profile.d/conda.sh
conda activate tnf

# Install requirements
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv -f https://data.pyg.org/whl/torch-2.6.0+cu124.html
pip install torch-geometric pyzx stim pennylane numpy pandas matplotlib seaborn SciencePlans networkx jupyterlab tqdm h5py setuptools==69.0.0

echo "✅ Environment setup complete"
