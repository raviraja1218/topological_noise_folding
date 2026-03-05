import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import TransformerConv, LayerNorm, global_mean_pool
from torch_geometric.data import Data
import numpy as np

class LaplacianPE(nn.Module):
    """Laplacian Positional Encoding"""
    def __init__(self, dim_pe=8):
        super().__init__()
        self.dim_pe = dim_pe
        
    def forward(self, edge_index, num_nodes):
        # Compute Laplacian eigenvectors (simplified)
        # In practice, this would compute actual eigenvectors
        pe = torch.randn(num_nodes, self.dim_pe, dtype=torch.float32)
        return pe

class GraphTransformer(nn.Module):
    def __init__(self, in_channels=32, hidden_channels=256, out_channels=1, 
                 num_layers=8, num_heads=8, dropout=0.1):
        super().__init__()
        
        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.out_channels = out_channels
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.dropout = dropout
        
        # Input projection - ensure float32
        self.input_proj = nn.Sequential(
            nn.Linear(in_channels, hidden_channels),
            nn.LayerNorm(hidden_channels),
            nn.Dropout(dropout)
        )
        
        # Laplacian PE
        self.laplacian_pe = LaplacianPE(dim_pe=8)
        self.pe_proj = nn.Linear(8, hidden_channels)
        
        # Graph Transformer layers
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        self.ffns = nn.ModuleList()
        
        for i in range(num_layers):
            self.convs.append(
                TransformerConv(
                    hidden_channels, 
                    hidden_channels // num_heads,
                    heads=num_heads,
                    dropout=dropout,
                    edge_dim=2  # Edge features: regular, Hadamard
                )
            )
            self.norms.append(nn.LayerNorm(hidden_channels))
            
            # FFN
            self.ffns.append(nn.Sequential(
                nn.Linear(hidden_channels, hidden_channels * 4),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_channels * 4, hidden_channels),
                nn.Dropout(dropout)
            ))
        
        # Output heads
        self.tcount_head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels // 2, 1)
        )
        
        self.gamma_head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels // 2, 1),
            nn.Sigmoid()  # Gamma between 0 and 1 (will scale)
        )
        
    def forward(self, x, edge_index, edge_attr, batch):
        # Ensure float32 dtype
        if x.dtype != torch.float32:
            x = x.float()
        if edge_attr.dtype != torch.float32:
            edge_attr = edge_attr.float()
            
        # Input projection
        x = self.input_proj(x)
        
        # Add Laplacian PE
        pe = self.laplacian_pe(edge_index, x.size(0))
        pe = pe.to(x.device)
        pe = self.pe_proj(pe)
        x = x + pe
        
        # Graph Transformer layers
        for conv, norm, ffn in zip(self.convs, self.norms, self.ffns):
            # Multi-head attention
            x_new = conv(x, edge_index, edge_attr)
            x_new = F.dropout(x_new, p=self.dropout, training=self.training)
            x = norm(x + x_new)
            
            # FFN
            x_new = ffn(x)
            x = norm(x + x_new)
        
        # Global pooling
        x_pool = global_mean_pool(x, batch)
        
        # Outputs
        tcount_pred = self.tcount_head(x_pool).squeeze(-1)
        gamma_pred = self.gamma_head(x_pool).squeeze(-1) * 2  # Scale to [0,2]
        
        return tcount_pred, gamma_pred
    
    def get_attention_weights(self, x, edge_index, edge_attr):
        """Extract attention weights for visualization"""
        attention_weights = []
        for conv in self.convs:
            # Forward pass with attention return
            x, (edge_index, attn) = conv(x, edge_index, edge_attr, return_attention_weights=True)
            attention_weights.append(attn)
        return attention_weights

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

if __name__ == "__main__":
    # Test the model
    model = GraphTransformer()
    print(f"Model created with {count_parameters(model):,} parameters")
    
    # Test forward pass with float32
    x = torch.randn(100, 32, dtype=torch.float32)
    edge_index = torch.randint(0, 100, (2, 200))
    edge_attr = torch.randn(200, 2, dtype=torch.float32)
    batch = torch.zeros(100, dtype=torch.long)
    
    tcount, gamma = model(x, edge_index, edge_attr, batch)
    print(f"Forward pass OK: tcount={tcount.item():.2f}, gamma={gamma.item():.3f}")
