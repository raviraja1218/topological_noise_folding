import multiprocessing as mp
import numpy as np
import torch
from collections import deque
import time
from pathlib import Path
import json
import pickle

class RolloutWorker:
    """Worker process for collecting rollouts"""
    
    def __init__(self, worker_id, env_creator, policy_fn, device='cpu'):
        self.worker_id = worker_id
        self.env_creator = env_creator
        self.policy_fn = policy_fn
        self.device = device
        self.env = None
        
    def initialize(self):
        """Initialize environment"""
        self.env = self.env_creator()
        
    def collect_rollout(self, max_steps=2048):
        """Collect rollout from environment"""
        if self.env is None:
            self.initialize()
            
        obs, _ = self.env.reset()
        rollout = []
        
        for step in range(max_steps):
            # Get action from policy
            action, log_prob, value = self.policy_fn(obs)
            
            # Step environment
            next_obs, reward, terminated, truncated, _ = self.env.step(action)
            done = terminated or truncated
            
            # Store transition
            rollout.append({
                'obs': obs,
                'action': action,
                'log_prob': log_prob,
                'value': value,
                'reward': reward,
                'done': done
            })
            
            obs = next_obs
            if done:
                break
                
        return rollout

class RolloutCollector:
    """Distributed rollout collection using multiprocessing"""
    
    def __init__(self, num_workers=12, env_creator=None, policy_fn=None, device='cuda'):
        self.num_workers = num_workers
        self.env_creator = env_creator
        self.policy_fn = policy_fn
        self.device = device
        self.workers = []
        self.pool = None
        
    def initialize_workers(self):
        """Initialize worker processes"""
        # Use spawn context for better compatibility
        ctx = mp.get_context('spawn')
        self.pool = ctx.Pool(processes=self.num_workers)
        
        # Create workers
        for i in range(self.num_workers):
            worker = RolloutWorker(i, self.env_creator, self.policy_fn, 'cpu')
            self.workers.append(worker)
            
    def collect_rollouts(self, num_steps=2048):
        """Collect rollouts from all workers in parallel"""
        if self.pool is None:
            self.initialize_workers()
            
        # Submit tasks
        results = []
        for i, worker in enumerate(self.workers):
            # Use apply_async with args
            result = self.pool.apply_async(self._worker_collect, args=(i, num_steps))
            results.append(result)
            
        # Collect results
        rollouts = []
        for result in results:
            try:
                rollout = result.get(timeout=30)
                rollouts.append(rollout)
            except Exception as e:
                print(f"Error collecting rollout: {e}")
                rollouts.append([])
            
        return rollouts
    
    def _worker_collect(self, worker_id, num_steps):
        """Helper method for worker collection"""
        worker = self.workers[worker_id]
        return worker.collect_rollout(num_steps)
    
    def shutdown(self):
        """Shutdown worker pool"""
        if self.pool:
            self.pool.close()
            self.pool.join()

class ReplayBuffer:
    """Replay buffer for storing trajectories"""
    
    def __init__(self, capacity=100000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        
    def push(self, trajectory):
        """Add trajectory to buffer"""
        self.buffer.extend(trajectory)
        
    def sample(self, batch_size):
        """Sample batch of transitions"""
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        batch = [self.buffer[i] for i in indices]
        return batch
    
    def clear(self):
        """Clear buffer"""
        self.buffer.clear()
        
    def __len__(self):
        return len(self.buffer)

class DistributedTrainer:
    """Trainer with distributed rollout collection"""
    
    def __init__(self, agent, env_creator, num_workers=12, buffer_size=100000):
        self.agent = agent
        self.env_creator = env_creator
        self.num_workers = num_workers
        self.buffer = ReplayBuffer(buffer_size)
        
        # Define policy function at class level (avoid local function)
        self.policy_fn = self._policy_fn
            
        self.collector = RolloutCollector(
            num_workers=num_workers,
            env_creator=env_creator,
            policy_fn=self.policy_fn
        )
    
    def _policy_fn(self, obs):
        """Policy function - defined at class level for pickling"""
        # Simplified policy for demonstration
        action = np.random.randint(0, 23)
        log_prob = 0.1
        value = 0.0
        return action, log_prob, value
        
    def train_step(self, steps_per_update=2048):
        """Perform one training step"""
        # Collect rollouts
        rollouts = self.collector.collect_rollouts(num_steps=steps_per_update)
        
        # Add to buffer
        for rollout in rollouts:
            self.buffer.push(rollout)
            
        # Sample batch
        batch = self.buffer.sample(batch_size=64)
        
        # Update agent
        loss = self.agent.update(batch)
        
        return {
            'loss': loss,
            'buffer_size': len(self.buffer),
            'rollouts_collected': len(rollouts)
        }
    
    def shutdown(self):
        """Shutdown collector"""
        self.collector.shutdown()

if __name__ == "__main__":
    print("Testing distributed rollout collection...")
    
    # Create dummy env creator
    def env_creator():
        from zx_env import ZXRewriteEnv
        return ZXRewriteEnv()
    
    # Create dummy agent
    class DummyAgent:
        def update(self, batch):
            return np.random.random()
    
    agent = DummyAgent()
    
    # Create trainer
    trainer = DistributedTrainer(agent, env_creator, num_workers=2)
    
    # Test training step
    for i in range(2):
        stats = trainer.train_step(steps_per_update=50)
        print(f"Step {i+1}: loss={stats['loss']:.4f}, buffer={stats['buffer_size']}")
        
    trainer.shutdown()
    print("✅ Distributed rollout test complete")
