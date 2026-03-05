#!/bin/bash

echo "=========================================================="
echo "PHASE 3 EXECUTION - GRAPH TRANSFORMER & NEURO-SYMBOLIC LOSS"
echo "=========================================================="
echo

# Step 3.1: Graph Transformer (test only)
echo "Testing Step 3.1: gnn_transformer.py"
python src/gnn_transformer.py
echo
read -p "Press Enter to continue to Step 3.2..."

# Step 3.2: Loss Function (test only)
echo "Testing Step 3.2: loss_function.py"
python src/loss_function.py
echo
read -p "Press Enter to continue to Step 3.3..."

# Step 3.3: Data Loader
echo "Running Step 3.3: graph_dataloader.py"
python src/graph_dataloader.py
echo
read -p "Press Enter to continue to Step 3.4..."

# Step 3.4: Small-Scale Training
echo "Running Step 3.4: train_small.py"
python src/train_small.py
echo
read -p "Press Enter to continue to Step 3.5..."

# Step 3.5: Loss Landscape Analysis
echo "Running Step 3.5: analyze_loss.py"
python src/analyze_loss.py

echo
echo "=========================================================="
echo "PHASE 3 EXECUTION COMPLETE"
echo "=========================================================="
