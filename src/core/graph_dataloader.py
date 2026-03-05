import torch
import numpy as np
import networkx as nx
import pickle
import os
from pathlib import Path
from torch_geometric.data import Data, Dataset, DataLoader
from torch_geometric.utils import from_networkx

class ZXGraphDataset(Dataset):
    """Dataset for ZX-diagrams from GraphML files"""
    
    def __init__(self, root, transform=None, pre_transform=None):
        self.root = root
        super().__init__(root, transform, pre_transform)
        
        # Find all graphml files
        self.graphml_dir = Path(root) / "baseline_graphs"
        self.graphml_files = list(self.graphml_dir.glob("*.graphml"))
        self.graphml_files.sort()
        
        # Load circuit metadata
        import pandas as pd
        self.metadata = pd.read_csv("results/baseline_tcounts.csv")
        
        print(f"Found {len(self.graphml_files)} graph files")
        
    def len(self):
        return len(self.graphml_files)
    
    def get(self, idx):
        # Load graphml file
        graphml_path = self.graphml_files[idx]
        circuit_name = graphml_path.stem
        
        # Load with networkx
        G = nx.read_graphml(graphml_path)
        
        # Convert node IDs to consecutive integers
        mapping = {node: i for i, node in enumerate(G.nodes())}
        G = nx.relabel_nodes(G, mapping)
        
        # Convert to PyG Data
        data = from_networkx(G)
        
        # Add node features (32-dim)
        num_nodes = data.num_nodes
        data.x = self.create_node_features(G, circuit_name, num_nodes)
        
        # Add edge features (2-dim: regular, Hadamard)
        data.edge_attr = self.create_edge_features(G, data.edge_index)
        
        # Add target values from metadata
        circuit_data = self.metadata[self.metadata['circuit_name'] == circuit_name].iloc[0]
        data.y_tcount = torch.tensor([circuit_data['t_count']], dtype=torch.float)
        
        # Theoretical gamma
        gamma = 1.00133
        data.y_gamma = torch.tensor([gamma], dtype=torch.float)
        
        # Store circuit info
        data.circuit_name = circuit_name
        data.num_qubits = circuit_data['qubits']
        
        return data
    
    def create_node_features(self, G, circuit_name, num_nodes):
        """Create 32-dim node features"""
        features = []
        
        for node in range(num_nodes):
            node_features = []
            
            # 1. Spider type (4-dim one-hot)
            # Default to Z-spider (simplified)
            spider_type = torch.zeros(4)
            spider_type[0] = 1.0  # Assume Z-spider
            node_features.append(spider_type)
            
            # 2. Phase angle (8-dim quantized)
            # Random phase for demonstration
            phase = torch.randn(8)
            node_features.append(phase)
            
            # 3. Connectivity degree (4-dim)
            degree = G.degree(node) if node in G else 0
            deg_feat = torch.tensor([
                degree / 100.0,  # normalized
                np.log(degree + 1) / 5.0,
                float(degree > 0),
                float(degree > 5)
            ])
            node_features.append(deg_feat)
            
            # 4. Pauli flow position (4-dim)
            flow_pos = torch.randn(4)  # Placeholder
            node_features.append(flow_pos)
            
            # 5. Laplacian PE (8-dim)
            laplacian_pe = torch.randn(8) * 0.1  # Placeholder
            node_features.append(laplacian_pe)
            
            # 6. Gate type indicators (4-dim)
            gate_type = torch.zeros(4)
            # Heuristic: T-gate if circuit contains T and node is special
            if 'hidden_shift' in circuit_name and node % 3 == 0:
                gate_type[0] = 1.0  # T-gate
            else:
                gate_type[1] = 1.0  # Clifford
            node_features.append(gate_type)
            
            # Concatenate all features (4+8+4+4+8+4 = 32)
            node_feat = torch.cat(node_features)
            features.append(node_feat)
        
        return torch.stack(features)
    
    def create_edge_features(self, G, edge_index):
        """Create 2-dim edge features"""
        num_edges = edge_index.size(1)
        
        # Random edge types for demonstration
        edge_attr = torch.zeros(num_edges, 2)
        
        # 70% regular edges, 30% Hadamard
        regular = torch.rand(num_edges) < 0.7
        edge_attr[regular, 0] = 1.0
        edge_attr[~regular, 1] = 1.0
        
        return edge_attr

def create_dataloaders(batch_size=32, val_split=0.2, test_split=0.1):
    """Create train/val/test dataloaders"""
    
    # Create dataset
    dataset = ZXGraphDataset(root="data/processed")
    
    # Split indices
    num_graphs = len(dataset)
    indices = np.random.permutation(num_graphs)
    
    val_size = int(val_split * num_graphs)
    test_size = int(test_split * num_graphs)
    train_size = num_graphs - val_size - test_size
    
    train_indices = indices[:train_size]
    val_indices = indices[train_size:train_size + val_size]
    test_indices = indices[train_size + val_size:]
    
    # Create subsets
    train_dataset = [dataset[i] for i in train_indices]
    val_dataset = [dataset[i] for i in val_indices]
    test_dataset = [dataset[i] for i in test_indices]
    
    # Dynamic batching function
    def collate_fn(batch):
        # Sort by number of nodes (for efficient batching)
        batch.sort(key=lambda x: x.num_nodes, reverse=True)
        return DataLoader.collate_fn(batch)
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True,
        collate_fn=collate_fn
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=batch_size,
        collate_fn=collate_fn
    )
    
    test_loader = DataLoader(
        test_dataset, 
        batch_size=batch_size,
        collate_fn=collate_fn
    )
    
    print(f"Dataset split: Train={len(train_dataset)}, Val={len(val_dataset)}, Test={len(test_dataset)}")
    
    return train_loader, val_loader, test_loader

if __name__ == "__main__":
    # Test the dataloader
    train_loader, val_loader, test_loader = create_dataloaders(batch_size=4)
    
    # Test one batch
    for batch in train_loader:
        print(f"Batch: {batch}")
        print(f"  Node features: {batch.x.shape}")
        print(f"  Edge index: {batch.edge_index.shape}")
        print(f"  Edge attributes: {batch.edge_attr.shape}")
        print(f"  T-count targets: {batch.y_tcount.shape}")
        print(f"  Batch assignment: {batch.batch.shape}")
        break
