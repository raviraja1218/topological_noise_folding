import pyzx as zx
import pickle
import os

print("=" * 60)
print("Adding GraphML Export Support")
print("=" * 60)

# Method 1: Use networkx as intermediate
try:
    import networkx as nx
    import pyzx as zx
    
    print("\n📄 Loading test graph...")
    with open("data/processed/test_graph.pickle", "rb") as f:
        g = pickle.load(f)
    
    print(f"✅ Graph loaded: {g.num_vertices()} vertices")
    
    # Convert to networkx
    nx_graph = nx.Graph()
    for v in range(g.num_vertices()):
        nx_graph.add_node(v)
    for e in g.edges():
        nx_graph.add_edge(e[0], e[1])
    
    # Save as GraphML
    nx.write_graphml(nx_graph, "data/processed/test_graph.graphml")
    print("✅ GraphML saved: data/processed/test_graph.graphml")
    
except ImportError:
    print("⚠️ networkx not installed. Installing...")
    os.system("pip install networkx")
    
    # Try again
    import networkx as nx
    with open("data/processed/test_graph.pickle", "rb") as f:
        g = pickle.load(f)
    
    nx_graph = nx.Graph()
    for v in range(g.num_vertices()):
        nx_graph.add_node(v)
    for e in g.edges():
        nx_graph.add_edge(e[0], e[1])
    
    nx.write_graphml(nx_graph, "data/processed/test_graph.graphml")
    print("✅ GraphML saved: data/processed/test_graph.graphml")

# Method 2: Try PyZX's internal method if available
try:
    print("\n🔄 Trying PyZX GraphML export...")
    # In some PyZX versions, this might work
    if hasattr(zx, 'graph_to_graphml'):
        zx.graph_to_graphml(g, "data/processed/test_graph_pyzx.graphml")
        print("✅ PyZX GraphML saved")
    else:
        print("⚠️ PyZX graph_to_graphml not available")
except Exception as e:
    print(f"⚠️ PyZX GraphML failed: {e}")

print("\n✅ GraphML export complete")
