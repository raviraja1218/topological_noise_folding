#!/bin/bash

echo "=========================================================="
echo "PHASE 4 EXECUTION - REINFORCEMENT LEARNING"
echo "=========================================================="
echo

# Step 4.1: ZX Environment
echo "Testing Step 4.1: zx_env.py"
python src/zx_env.py
echo
read -p "Press Enter to continue to Step 4.2..."

# Step 4.2: PPO Agent
echo "Testing Step 4.2: ppo_agent.py"
python src/ppo_agent.py
echo
read -p "Press Enter to continue to Step 4.3..."

# Step 4.3: Action Masking
echo "Testing Step 4.3: action_masking.py"
python src/action_masking.py
echo
read -p "Press Enter to continue to Step 4.4..."

# Step 4.4: Curriculum Learning
echo "Running Step 4.4: curriculum.py"
python src/curriculum.py
echo
read -p "Press Enter to continue to Step 4.5..."

# Step 4.5: Distributed Rollout
echo "Testing Step 4.5: rollout_collector.py"
python src/rollout_collector.py
echo
read -p "Press Enter to continue to Step 4.6..."

# Step 4.6: Validation
echo "Running Step 4.6: validate_agent.py"
python src/validate_agent.py

echo
echo "=========================================================="
echo "PHASE 4 EXECUTION COMPLETE"
echo "=========================================================="
