import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import numpy as np
import pandas as pd
from pathlib import Path
import time
import json
from datetime import datetime

# Import our modules
from gnn_transformer import GraphTransformer, count_parameters
from loss_function import NeuroSymbolicLoss
from graph_dataloader import create_dataloaders

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
if device.type == 'cuda':
    print(f"  GPU: {torch.cuda.get_device_name(0)}")
    print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Create directories
Path("checkpoints").mkdir(exist_ok=True)
Path("results").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

# Hyperparameters
config = {
    'in_channels': 32,
    'hidden_channels': 256,
    'out_channels': 1,
    'num_layers': 8,
    'num_heads': 8,
    'dropout': 0.1,
    'batch_size': 32,
    'learning_rate': 1e-4,
    'weight_decay': 1e-5,
    'epochs': 100,
    'lambda_init': 0.1,
    'tcount_weight': 0.7,
    'gamma_weight': 0.3,
    'val_split': 0.2,
    'test_split': 0.1,
    'seed': 42
}

# Set seed
torch.manual_seed(config['seed'])
np.random.seed(config['seed'])

def train_epoch(model, loader, loss_fn, optimizer, epoch):
    model.train()
    total_loss = 0
    total_task_loss = 0
    total_symbolic_loss = 0
    num_batches = 0
    penalty_active_batches = 0
    
    for batch in loader:
        batch = batch.to(device)
        
        # Ensure float32 for all tensors
        if batch.x.dtype != torch.float32:
            batch.x = batch.x.float()
        if hasattr(batch, 'edge_attr') and batch.edge_attr.dtype != torch.float32:
            batch.edge_attr = batch.edge_attr.float()
        
        # Forward pass
        tcount_pred, gamma_pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)
        
        # Get targets - ensure float32
        tcount_true = batch.y_tcount.squeeze().float()
        gamma_true = batch.y_gamma.squeeze().float()
        
        # Compute loss
        loss, log_dict = loss_fn(
            tcount_pred, gamma_pred, tcount_true, gamma_true,
            [batch], epoch=epoch, training=True
        )
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        # Track metrics
        total_loss += log_dict['loss_total']
        total_task_loss += log_dict['loss_task']
        total_symbolic_loss += log_dict['loss_symbolic']
        num_batches += 1
        
        if log_dict['loss_symbolic'] > 0:
            penalty_active_batches += 1
    
    # Record GPU memory
    if device.type == 'cuda':
        vram_used = torch.cuda.max_memory_allocated(device) / 1e9
        torch.cuda.reset_peak_memory_stats()
    else:
        vram_used = 0
    
    return {
        'loss': total_loss / num_batches,
        'task_loss': total_task_loss / num_batches,
        'symbolic_loss': total_symbolic_loss / num_batches,
        'penalty_rate': penalty_active_batches / num_batches,
        'vram_gb': vram_used
    }

def validate(model, loader, loss_fn, epoch):
    model.eval()
    total_loss = 0
    total_task_loss = 0
    total_symbolic_loss = 0
    num_batches = 0
    predictions = []
    targets = []
    
    with torch.no_grad():
        for batch in loader:
            batch = batch.to(device)
            
            # Ensure float32
            if batch.x.dtype != torch.float32:
                batch.x = batch.x.float()
            if hasattr(batch, 'edge_attr') and batch.edge_attr.dtype != torch.float32:
                batch.edge_attr = batch.edge_attr.float()
            
            # Forward pass
            tcount_pred, gamma_pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)
            
            # Get targets
            tcount_true = batch.y_tcount.squeeze().float()
            gamma_true = batch.y_gamma.squeeze().float()
            
            # Compute loss
            loss, log_dict = loss_fn(
                tcount_pred, gamma_pred, tcount_true, gamma_true,
                [batch], epoch=epoch, training=False
            )
            
            # Track metrics
            total_loss += log_dict['loss_total']
            total_task_loss += log_dict['loss_task']
            total_symbolic_loss += log_dict['loss_symbolic']
            num_batches += 1
            
            # Store predictions
            predictions.extend(tcount_pred.cpu().numpy())
            targets.extend(tcount_true.cpu().numpy())
    
    # Compute accuracy metrics
    predictions = np.array(predictions)
    targets = np.array(targets)
    mae = np.mean(np.abs(predictions - targets))
    mape = np.mean(np.abs((predictions - targets) / (targets + 1))) * 100
    
    return {
        'loss': total_loss / num_batches,
        'task_loss': total_task_loss / num_batches,
        'symbolic_loss': total_symbolic_loss / num_batches,
        'mae': mae,
        'mape': mape
    }

def main():
    print("=" * 60)
    print("PHASE 3: Graph Transformer Training (Fixed)")
    print("=" * 60)
    print(f"\nConfiguration:")
    for k, v in config.items():
        print(f"  {k}: {v}")
    
    # Create dataloaders
    print("\n📂 Creating dataloaders...")
    train_loader, val_loader, test_loader = create_dataloaders(
        batch_size=config['batch_size'],
        val_split=config['val_split'],
        test_split=config['test_split']
    )
    
    # Create model
    print("\n🏗️  Building Graph Transformer...")
    model = GraphTransformer(
        in_channels=config['in_channels'],
        hidden_channels=config['hidden_channels'],
        out_channels=config['out_channels'],
        num_layers=config['num_layers'],
        num_heads=config['num_heads'],
        dropout=config['dropout']
    ).to(device)
    
    num_params = count_parameters(model)
    print(f"  Parameters: {num_params:,}")
    
    # Create loss function
    loss_fn = NeuroSymbolicLoss(
        lambda_init=config['lambda_init'],
        tcount_weight=config['tcount_weight'],
        gamma_weight=config['gamma_weight']
    )
    
    # Create optimizer
    optimizer = optim.AdamW(
        model.parameters(),
        lr=config['learning_rate'],
        weight_decay=config['weight_decay']
    )
    
    # Create scheduler
    scheduler = ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=10, verbose=True
    )
    
    # Training loop
    print("\n🚀 Starting training...")
    print("-" * 60)
    
    history = {
        'train_loss': [], 'val_loss': [],
        'train_task': [], 'val_task': [],
        'train_symbolic': [], 'val_symbolic': [],
        'penalty_rate': [], 'vram_gb': [],
        'val_mae': [], 'val_mape': [],
        'learning_rate': []
    }
    
    best_val_loss = float('inf')
    best_epoch = 0
    
    for epoch in range(1, config['epochs'] + 1):
        # Train
        train_metrics = train_epoch(model, train_loader, loss_fn, optimizer, epoch)
        
        # Validate
        val_metrics = validate(model, val_loader, loss_fn, epoch)
        
        # Update scheduler
        scheduler.step(val_metrics['loss'])
        current_lr = optimizer.param_groups[0]['lr']
        
        # Save history
        history['train_loss'].append(train_metrics['loss'])
        history['val_loss'].append(val_metrics['loss'])
        history['train_task'].append(train_metrics['task_loss'])
        history['val_task'].append(val_metrics['task_loss'])
        history['train_symbolic'].append(train_metrics['symbolic_loss'])
        history['val_symbolic'].append(val_metrics['symbolic_loss'])
        history['penalty_rate'].append(train_metrics['penalty_rate'])
        history['vram_gb'].append(train_metrics['vram_gb'])
        history['val_mae'].append(val_metrics['mae'])
        history['val_mape'].append(val_metrics['mape'])
        history['learning_rate'].append(current_lr)
        
        # Print progress
        if epoch % 5 == 0 or epoch == 1:
            print(f"\nEpoch {epoch}/{config['epochs']}:")
            print(f"  Train Loss: {train_metrics['loss']:.2f} (Task: {train_metrics['task_loss']:.2f}, Sym: {train_metrics['symbolic_loss']:.4f})")
            print(f"  Val Loss:   {val_metrics['loss']:.2f} (Task: {val_metrics['task_loss']:.2f}, Sym: {val_metrics['symbolic_loss']:.4f})")
            print(f"  Penalty Rate: {train_metrics['penalty_rate']*100:.1f}%")
            print(f"  Val MAE: {val_metrics['mae']:.1f} T-gates")
            print(f"  VRAM: {train_metrics['vram_gb']:.2f} GB")
            print(f"  LR: {current_lr:.2e}")
        
        # Save best model
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            best_epoch = epoch
            
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_metrics['loss'],
                'val_mae': val_metrics['mae'],
                'config': config
            }
            torch.save(checkpoint, 'checkpoints/gnn_small_v1.pt')
            print(f"  ✅ Best model saved (epoch {epoch})")
    
    print("\n" + "=" * 60)
    print("✅ Training complete!")
    print(f"Best epoch: {best_epoch}, Best val loss: {best_val_loss:.2f}")
    
    # Save training history
    history_df = pd.DataFrame(history)
    history_df.to_csv('results/phase3_training_logs.csv', index=False)
    print("✅ Training logs saved to results/phase3_training_logs.csv")
    
    # Save hyperparameters
    with open('results/hyperparameters.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Also save as CSV for paper
    hyper_df = pd.DataFrame([config])
    hyper_df.to_csv('results/hyperparameters.csv', index=False)
    print("✅ Hyperparameters saved to results/hyperparameters.csv")
    
    # Final test evaluation
    print("\n📊 Final test evaluation:")
    test_metrics = validate(model, test_loader, loss_fn, config['epochs'])
    print(f"  Test Loss: {test_metrics['loss']:.2f}")
    print(f"  Test MAE: {test_metrics['mae']:.1f} T-gates")
    print(f"  Test MAPE: {test_metrics['mape']:.1f}%")
    
    return model, history

if __name__ == "__main__":
    model, history = main()
