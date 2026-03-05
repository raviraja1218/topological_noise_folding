import numpy as np
from pathlib import Path
import json

class CurriculumScheduler:
    """Curriculum learning scheduler for progressive training"""
    
    def __init__(self, total_epochs=400):
        self.total_epochs = total_epochs
        
        # Define curriculum stages
        self.stages = [
            {
                'name': 'Stage 1: Small circuits (5-20 qubits)',
                'epoch_range': (0, 100),
                'circuit_range': (5, 20),
                'exploration_temp': 1.0,
                'batch_size': 32,
                'reward_scale': 1.0,
                'circuit_families': ['arithmetic', 'bv']
            },
            {
                'name': 'Stage 2: Medium circuits (20-65 qubits)',
                'epoch_range': (101, 200),
                'circuit_range': (20, 65),
                'exploration_temp': 0.8,
                'batch_size': 24,
                'reward_scale': 1.2,
                'circuit_families': ['mod5', 'oracle']
            },
            {
                'name': 'Stage 3: Large circuits (65-127 qubits)',
                'epoch_range': (201, 300),
                'circuit_range': (65, 127),
                'exploration_temp': 0.6,
                'batch_size': 16,
                'reward_scale': 1.5,
                'circuit_families': ['qaoa']
            },
            {
                'name': 'Stage 4: XL circuits (127-768 qubits)',
                'epoch_range': (301, 400),
                'circuit_range': (127, 768),
                'exploration_temp': 0.4,
                'batch_size': 8,
                'reward_scale': 2.0,
                'circuit_families': ['hidden_shift']
            }
        ]
        
    def get_stage(self, epoch):
        """Get current stage based on epoch"""
        for stage in self.stages:
            start, end = stage['epoch_range']
            if start <= epoch <= end:
                return stage
        return self.stages[-1]  # Default to last stage
    
    def get_parameters(self, epoch):
        """Get curriculum parameters for current epoch"""
        stage = self.get_stage(epoch)
        
        # Linear annealing within stage
        start, end = stage['epoch_range']
        progress = (epoch - start) / (end - start) if end > start else 0
        
        # Exploration temperature annealing
        base_temp = stage['exploration_temp']
        temp = base_temp * (1 - 0.5 * progress)  # Anneal by up to 50%
        
        # Learning rate multiplier
        lr_mult = 1.0 - 0.5 * progress  # Decrease LR over time
        
        return {
            'stage_name': stage['name'],
            'exploration_temp': max(0.1, temp),
            'batch_size': stage['batch_size'],
            'reward_scale': stage['reward_scale'],
            'lr_multiplier': lr_mult,
            'circuit_range': stage['circuit_range'],
            'circuit_families': stage['circuit_families']
        }
    
    def select_circuit(self, epoch, available_circuits):
        """Select appropriate circuit for current stage"""
        params = self.get_parameters(epoch)
        
        # Filter circuits by qubit range
        min_q, max_q = params['circuit_range']
        families = params['circuit_families']
        
        eligible = []
        for circuit in available_circuits:
            qubits = circuit.get('qubits', 0)
            family = circuit.get('family', '')
            
            if min_q <= qubits <= max_q and family in families:
                eligible.append(circuit)
        
        if eligible:
            return np.random.choice(len(eligible))
        else:
            return 0
    
    def get_learning_rate(self, base_lr, epoch):
        """Get curriculum-adjusted learning rate"""
        params = self.get_parameters(epoch)
        return base_lr * params['lr_multiplier']
    
    def save_schedule(self, path):
        """Save curriculum schedule to JSON"""
        schedule = []
        for epoch in range(1, self.total_epochs + 1):
            params = self.get_parameters(epoch)
            schedule.append({
                'epoch': epoch,
                'stage': params['stage_name'],
                'exploration_temp': params['exploration_temp'],
                'batch_size': params['batch_size'],
                'reward_scale': params['reward_scale']
            })
        
        with open(path, 'w') as f:
            json.dump(schedule, f, indent=2)
        
        print(f"✅ Curriculum schedule saved to {path}")

class CurriculumTrainer:
    """Trainer with curriculum learning"""
    
    def __init__(self, agent, envs, curriculum, device='cuda'):
        self.agent = agent
        self.envs = envs
        self.curriculum = curriculum
        self.device = device
        
    def train_epoch(self, epoch):
        """Train for one epoch with curriculum"""
        params = self.curriculum.get_parameters(epoch)
        
        print(f"\nEpoch {epoch}: {params['stage_name']}")
        print(f"  temp={params['exploration_temp']:.2f}, batch={params['batch_size']}, scale={params['reward_scale']:.2f}")
        
        # Update agent parameters
        self.agent.exploration_temp = params['exploration_temp']
        
        # Collect trajectories
        trajectories = self.collect_trajectories(params['batch_size'])
        
        # Update policy
        loss = self.agent.update(trajectories)
        
        return loss
    
    def collect_trajectories(self, batch_size):
        """Collect trajectories from environments"""
        # Simplified collection
        trajectories = []
        for _ in range(batch_size):
            # Random trajectory for demonstration
            traj = {
                'states': np.random.randn(10, 32),
                'actions': np.random.randint(0, 23, 10),
                'rewards': np.random.randn(10),
                'dones': np.zeros(10)
            }
            trajectories.append(traj)
        return trajectories

if __name__ == "__main__":
    # Test curriculum scheduler
    curriculum = CurriculumScheduler(total_epochs=400)
    
    print("Curriculum Learning Schedule:")
    print("-" * 60)
    
    for epoch in [1, 50, 150, 250, 350, 400]:
        params = curriculum.get_parameters(epoch)
        print(f"Epoch {epoch}:")
        print(f"  {params['stage_name']}")
        print(f"  temp={params['exploration_temp']:.2f}, batch={params['batch_size']}")
        print(f"  families: {params['circuit_families']}")
    
    # Save schedule
    curriculum.save_schedule('results/curriculum_schedule.json')
