import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class NeuroSymbolicLoss(nn.Module):
    def __init__(self, lambda_init=0.1, tcount_weight=0.7, gamma_weight=0.3):
        super().__init__()
        self.lambda_init = lambda_init
        self.tcount_weight = tcount_weight
        self.gamma_weight = gamma_weight
        self.mse = nn.MSELoss()
        
    def forward(self, tcount_pred, gamma_pred, tcount_true, gamma_true, 
                graphs, epoch=None, training=True):
        """
        Args:
            tcount_pred: Predicted T-count [batch]
            gamma_pred: Predicted gamma [batch]
            tcount_true: Ground truth T-count [batch]
            gamma_true: Ground truth gamma [batch]
            graphs: List of graph data objects with M, N, C matrices
            epoch: Current epoch for lambda scheduling
            training: Whether in training mode
        """
        # Task loss
        loss_tcount = self.mse(tcount_pred, tcount_true)
        loss_gamma = self.mse(gamma_pred, gamma_true)
        loss_task = self.tcount_weight * loss_tcount + self.gamma_weight * loss_gamma
        
        # Symbolic penalty
        loss_symbolic = self.compute_symbolic_penalty(graphs, tcount_pred.device)
        
        # Lambda scheduling
        lambda_val = self.get_lambda(epoch) if epoch is not None else self.lambda_init
        
        # Total loss
        loss_total = loss_task + lambda_val * loss_symbolic
        
        # Logging dict
        log_dict = {
            'loss_total': loss_total.item(),
            'loss_task': loss_task.item(),
            'loss_symbolic': loss_symbolic.item(),
            'loss_tcount': loss_tcount.item(),
            'loss_gamma': loss_gamma.item(),
            'lambda': lambda_val
        }
        
        return loss_total, log_dict
    
    def compute_symbolic_penalty(self, graphs, device):
        """Compute symbolic penalty based on Pauli flow"""
        batch_size = len(graphs)
        penalties = []
        
        for graph in graphs:
            if hasattr(graph, 'M') and hasattr(graph, 'N') and hasattr(graph, 'C'):
                # Get matrices
                M = graph.M  # Flow-demand matrix
                N = graph.N  # Order-demand matrix
                C = graph.C  # Connectivity matrix
                
                # Compute NC product
                NC = torch.mm(N, C)
                n = NC.size(0)
                
                # Check if DAG using matrix exponential trace
                # Tr(e^NC) > n indicates cycles
                try:
                    exp_NC = torch.matrix_exp(NC)
                    trace_exp = torch.trace(exp_NC)
                    
                    if torch.abs(trace_exp - n) < 1e-5:
                        # DAG - no penalty
                        penalty = torch.tensor(0.0, device=device)
                    else:
                        # Cycles detected
                        violation_count = torch.sum(torch.abs(exp_NC - torch.eye(n, device=device)) > 1e-5)
                        penalty = 1.0 + violation_count / (n * n)
                except:
                    # If matrix_exp fails, use approximate check
                    # Count diagonal entries > 1 in powers
                    NC_power = NC.clone()
                    cycles_detected = False
                    for k in range(2, min(5, n)):  # Check up to 4-cycles
                        NC_power = torch.mm(NC_power, NC)
                        if torch.any(torch.diag(NC_power) > 1e-5):
                            cycles_detected = True
                            break
                    
                    if cycles_detected:
                        penalty = torch.tensor(2.0, device=device)
                    else:
                        penalty = torch.tensor(0.0, device=device)
            else:
                # No flow matrices - assume invalid (high penalty)
                penalty = torch.tensor(10.0, device=device)
            
            penalties.append(penalty)
        
        return torch.stack(penalties).mean()
    
    def get_lambda(self, epoch):
        """Schedule lambda based on training stage"""
        if epoch < 10:  # Warmup
            return 0.01
        elif epoch < 50:  # Main training
            return 0.1
        else:  # Fine-tuning
            return 0.5

class SymbolicPenalty(nn.Module):
    """Standalone symbolic penalty for validation"""
    def __init__(self):
        super().__init__()
        
    def forward(self, M, N, C):
        """
        Check if NC forms DAG
        Returns: penalty (0 if DAG, >0 if cycles)
        """
        n = C.size(0)
        NC = torch.mm(N, C)
        
        # Check if NC is acyclic using trace of exponential
        try:
            exp_NC = torch.matrix_exp(NC)
            trace_exp = torch.trace(exp_NC)
            
            if torch.abs(trace_exp - n) < 1e-5:
                return torch.tensor(0.0, device=NC.device), True
            else:
                return trace_exp - n, False
        except:
            # Fallback: check powers
            NC_power = NC.clone()
            for k in range(2, min(10, n)):
                NC_power = torch.mm(NC_power, NC)
                if torch.any(torch.diag(NC_power) > 1e-5):
                    return torch.tensor(float(k), device=NC.device), False
            return torch.tensor(0.0, device=NC.device), True

if __name__ == "__main__":
    # Test the loss function
    loss_fn = NeuroSymbolicLoss()
    
    # Dummy data
    tcount_pred = torch.tensor([100.0, 200.0])
    gamma_pred = torch.tensor([1.001, 1.002])
    tcount_true = torch.tensor([120.0, 220.0])
    gamma_true = torch.tensor([1.00133, 1.00133])
    
    # Dummy graphs
    graphs = []
    for i in range(2):
        graph = type('Graph', (), {})()
        graph.M = torch.randn(10, 10)
        graph.N = torch.randn(10, 10)
        graph.C = torch.randn(10, 10)
        graphs.append(graph)
    
    loss_total, log_dict = loss_fn(tcount_pred, gamma_pred, tcount_true, 
                                    gamma_true, graphs, epoch=25)
    
    print("Loss function test:")
    for k, v in log_dict.items():
        print(f"  {k}: {v:.4f}")
