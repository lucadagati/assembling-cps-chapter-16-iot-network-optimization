# Usage Examples

This document provides comprehensive examples of how to use the IoT network optimization package for various scenarios.

## Quick Start

### Basic Installation and Setup

```python
# Install dependencies
pip install -r requirements.txt

# Import the main package
from src import IoTGraph, Node, Edge, NodeType
from src.algorithms import solve_steiner_tree_constrained, compare_mst_algorithms
from src.utils import GraphGenerator
from src.visualization import NetworkPlotter
```

### Creating a Simple Network

```python
# Create a simple IoT network
graph = IoTGraph()

# Add nodes
weak_node = Node(0, NodeType.WEAK, capacity=1, computational_power=0.8)
mandatory_node = Node(1, NodeType.MANDATORY, capacity=3, computational_power=0.2)
discretionary_node = Node(2, NodeType.DISCRETIONARY, capacity=2, computational_power=0.5)

graph.add_node(weak_node)
graph.add_node(mandatory_node)
graph.add_node(discretionary_node)

# Add edges
graph.add_edge(Edge(0, 1, 5.0))  # Weak to mandatory
graph.add_edge(Edge(0, 2, 3.0))  # Weak to discretionary
graph.add_edge(Edge(1, 2, 2.0))  # Mandatory to discretionary
```

## Algorithm Usage

### Minimum Spanning Tree (MST) Algorithms

```python
from src.algorithms import KruskalMST, PrimMST, ConstrainedMST

# Kruskal's algorithm
kruskal = KruskalMST(graph)
kruskal_solution = kruskal.solve()
print(f"Kruskal MST cost: {kruskal_solution.total_cost:.2f}")

# Prim's algorithm
prim = PrimMST(graph)
prim_solution = prim.solve()
print(f"Prim MST cost: {prim_solution.total_cost:.2f}")

# Constrained MST
constrained = ConstrainedMST(graph)
constrained_solution = constrained.solve()
print(f"Constrained MST cost: {constrained_solution.total_cost:.2f}")
```

### Steiner Tree Algorithm

```python
from src.algorithms import solve_steiner_tree_constrained

# Solve constrained Steiner Tree problem
steiner_solution = solve_steiner_tree_constrained(graph)

print(f"Steiner Tree cost: {steiner_solution.total_cost:.2f}")
print(f"Connected nodes: {len(steiner_solution.connected_nodes)}")
print(f"Capacity violations: {steiner_solution.capacity_violations}")
print(f"Unconnected weak nodes: {len(steiner_solution.unconnected_weak_nodes)}")
```

### Algorithm Comparison

```python
from src.algorithms import compare_mst_algorithms

# Compare different MST algorithms
mst_results = compare_mst_algorithms(graph)

for name, solution in mst_results.items():
    print(f"{name}: Cost = {solution.total_cost:.2f}, Edges = {len(solution.edges)}")
```

## Network Generation

### Random Network Generation

```python
from src.utils import GraphGenerator

# Create a random IoT network
generator = GraphGenerator(seed=42)
graph = generator.generate_random_iot_network(
    num_weak=10,           # Number of weak nodes
    num_mandatory=3,       # Number of mandatory nodes
    num_discretionary=2,   # Number of discretionary nodes
    connection_probability=0.4,  # Probability of edge existence
    weight_range=(1.0, 10.0),    # Range for edge weights
    capacity_range=(2, 5)        # Range for node capacities
)
```

### Specialized Network Generation

```python
# Fire detection network
fire_network = generator.generate_fire_detection_network()

# Drone coordination network
drone_network = generator.generate_drone_network()

# Grid-based network
grid_network = generator.generate_grid_iot_network(grid_size=6)
```

### Sample Networks

```python
from data.sample_networks import get_sample_networks

# Get pre-defined sample networks
networks = get_sample_networks()
simple_network = networks["simple"]
medium_network = networks["medium"]
large_network = networks["large"]
```

## Visualization

### Basic Network Visualization

```python
from src.visualization import NetworkPlotter

# Create plotter
plotter = NetworkPlotter()

# Plot original network
plotter.plot_network(graph, title="Original IoT Network")

# Plot MST solution
plotter.plot_mst_solution(graph, kruskal_solution, title="Kruskal MST Solution")

# Plot Steiner Tree solution
plotter.plot_steiner_solution(graph, steiner_solution, title="Steiner Tree Solution")
```

### Algorithm Comparison Visualization

```python
# Compare algorithms visually
plotter.plot_algorithm_comparison(
    graph, 
    mst_results, 
    steiner_solution,
    title="Algorithm Comparison"
)

# Cost comparison chart
plotter.plot_cost_comparison(
    mst_results, 
    steiner_solution,
    title="Cost Comparison"
)
```

## Real-World Applications

### Fire Detection System

```python
# Create fire detection network
generator = GraphGenerator(seed=42)
fire_network = generator.generate_fire_detection_network()

# Optimize the network
steiner_solution = solve_steiner_tree_constrained(fire_network)

# Analyze performance
total_sensors = len(fire_network.get_nodes_by_type(NodeType.WEAK))
connected_sensors = total_sensors - len(steiner_solution.unconnected_weak_nodes)
connectivity_rate = (connected_sensors / total_sensors) * 100

print(f"Fire Detection Network:")
print(f"  Total sensors: {total_sensors}")
print(f"  Connected sensors: {connected_sensors}")
print(f"  Connectivity rate: {connectivity_rate:.1f}%")
```

### Drone Coordination System

```python
# Create drone network
drone_network = generator.generate_drone_network()

# Optimize for drone operations
steiner_solution = solve_steiner_tree_constrained(drone_network)

# Analyze drone network performance
control_nodes = drone_network.get_nodes_by_type(NodeType.MANDATORY)
total_capacity = sum(node.capacity for node in control_nodes)
used_capacity = sum(
    len(drone_network.get_neighbors(node.id)) 
    for node in control_nodes 
    if node.id in steiner_solution.connected_nodes
)

print(f"Drone Network:")
print(f"  Control stations: {len(control_nodes)}")
print(f"  Total capacity: {total_capacity}")
print(f"  Used capacity: {used_capacity}")
print(f"  Utilization: {(used_capacity/total_capacity)*100:.1f}%")
```

### IoT Sensor Network

```python
# Create sensor network
sensor_network = generator.generate_random_iot_network(
    num_weak=15, num_mandatory=4, num_discretionary=3
)

# Optimize the network
steiner_solution = solve_steiner_tree_constrained(sensor_network)

# Simulate data collection
sensor_nodes = sensor_network.get_nodes_by_type(NodeType.WEAK)
connected_sensors = [s for s in sensor_nodes if s.id in steiner_solution.connected_nodes]

print(f"Sensor Network:")
print(f"  Total sensors: {len(sensor_nodes)}")
print(f"  Connected sensors: {len(connected_sensors)}")
print(f"  Data collection rate: {len(connected_sensors)/len(sensor_nodes)*100:.1f}%")
```

## Advanced Usage

### Custom Objective Function

```python
# Customize the objective function parameters
steiner_solution = solve_steiner_tree_constrained(graph)

# Calculate objective function with different alpha values
alpha_0 = steiner_solution.get_score(alpha=0.0)    # Focus on operation costs
alpha_1 = steiner_solution.get_score(alpha=1.0)    # Focus on connection costs
alpha_05 = steiner_solution.get_score(alpha=0.5)   # Balanced approach

print(f"Objective function scores:")
print(f"  Alpha=0.0 (operation focus): {alpha_0:.3f}")
print(f"  Alpha=1.0 (connection focus): {alpha_1:.3f}")
print(f"  Alpha=0.5 (balanced): {alpha_05:.3f}")
```

### Network Analysis

```python
# Analyze network properties
print(f"Network Analysis:")
print(f"  Total nodes: {len(graph.nodes)}")
print(f"  Total edges: {len(graph.edges) // 2}")
print(f"  Is connected: {graph.is_connected()}")

# Analyze node types
weak_nodes = graph.get_nodes_by_type(NodeType.WEAK)
mandatory_nodes = graph.get_nodes_by_type(NodeType.MANDATORY)
discretionary_nodes = graph.get_nodes_by_type(NodeType.DISCRETIONARY)

print(f"  Weak nodes: {len(weak_nodes)}")
print(f"  Mandatory nodes: {len(mandatory_nodes)}")
print(f"  Discretionary nodes: {len(discretionary_nodes)}")

# Analyze capacity utilization
total_capacity = sum(node.capacity for node in graph.nodes.values() if node.capacity)
print(f"  Total capacity: {total_capacity}")
```

### Path Finding

```python
# Find shortest path between nodes
source = 0
target = 5
path = graph.get_shortest_path(source, target)

if path:
    path_cost = graph.get_path_cost(path)
    print(f"Shortest path from {source} to {target}:")
    print(f"  Path: {' -> '.join(map(str, path))}")
    print(f"  Cost: {path_cost:.2f}")
else:
    print(f"No path found from {source} to {target}")
```

## Performance Optimization

### Large Network Handling

```python
# For large networks, consider using faster algorithms
large_graph = generator.generate_random_iot_network(
    num_weak=50, num_mandatory=10, num_discretionary=5
)

# Use Prim's algorithm for dense graphs
prim = PrimMST(large_graph)
prim_solution = prim.solve()

# Use Kruskal's algorithm for sparse graphs
kruskal = KruskalMST(large_graph)
kruskal_solution = kruskal.solve()

print(f"Large network optimization:")
print(f"  Prim's cost: {prim_solution.total_cost:.2f}")
print(f"  Kruskal's cost: {kruskal_solution.total_cost:.2f}")
```

### Memory Optimization

```python
# For memory-constrained environments
import gc

# Process networks in batches
networks = get_sample_networks()
for name, network in networks.items():
    solution = solve_steiner_tree_constrained(network)
    print(f"{name}: {solution.total_cost:.2f}")
    
    # Clean up memory
    del solution
    gc.collect()
```

## Error Handling

### Robust Network Processing

```python
def safe_optimize_network(graph):
    """Safely optimize a network with error handling."""
    try:
        # Check if graph is valid
        if not graph.nodes:
            raise ValueError("Empty graph")
        
        if not graph.is_connected():
            print("Warning: Graph is not connected")
        
        # Optimize the network
        solution = solve_steiner_tree_constrained(graph)
        
        # Validate solution
        if solution.total_cost < 0:
            raise ValueError("Invalid solution cost")
        
        return solution
        
    except Exception as e:
        print(f"Error optimizing network: {e}")
        return None

# Usage
solution = safe_optimize_network(graph)
if solution:
    print(f"Optimization successful: {solution.total_cost:.2f}")
else:
    print("Optimization failed")
```

## Integration with External Systems

### Export to NetworkX

```python
import networkx as nx

# Convert to NetworkX for additional analysis
nx_graph = graph.to_networkx()

# Use NetworkX algorithms
centrality = nx.betweenness_centrality(nx_graph)
clustering = nx.clustering(nx_graph)

print("NetworkX Analysis:")
print(f"  Average clustering: {sum(clustering.values()) / len(clustering):.3f}")
print(f"  Max centrality: {max(centrality.values()):.3f}")
```

### Data Export

```python
import json
import pandas as pd

# Export network data
network_data = {
    'nodes': [
        {
            'id': node.id,
            'type': node.node_type.value,
            'capacity': node.capacity,
            'computational_power': node.computational_power
        }
        for node in graph.nodes.values()
    ],
    'edges': [
        {
            'source': edge.source,
            'target': edge.target,
            'weight': edge.weight
        }
        for edge in graph.edges.values()
        if edge.source < edge.target  # Avoid duplicates
    ]
}

# Save to JSON
with open('network_data.json', 'w') as f:
    json.dump(network_data, f, indent=2)

# Create DataFrame for analysis
nodes_df = pd.DataFrame(network_data['nodes'])
edges_df = pd.DataFrame(network_data['edges'])

print("Network exported successfully!")
```

## Best Practices

### Code Organization

```python
class NetworkOptimizer:
    """Wrapper class for network optimization operations."""
    
    def __init__(self, graph):
        self.graph = graph
        self.solutions = {}
    
    def optimize_all(self):
        """Run all optimization algorithms."""
        # MST algorithms
        from src.algorithms import compare_mst_algorithms
        self.solutions['mst'] = compare_mst_algorithms(self.graph)
        
        # Steiner Tree
        self.solutions['steiner'] = solve_steiner_tree_constrained(self.graph)
        
        return self.solutions
    
    def get_best_solution(self):
        """Get the best solution based on cost."""
        if not self.solutions:
            self.optimize_all()
        
        best_mst = min(self.solutions['mst'].values(), key=lambda x: x.total_cost)
        steiner = self.solutions['steiner']
        
        if best_mst.total_cost <= steiner.total_cost:
            return best_mst
        else:
            return steiner
    
    def visualize_results(self):
        """Visualize all results."""
        plotter = NetworkPlotter()
        
        if 'mst' in self.solutions and 'steiner' in self.solutions:
            plotter.plot_algorithm_comparison(
                self.graph,
                self.solutions['mst'],
                self.solutions['steiner']
            )

# Usage
optimizer = NetworkOptimizer(graph)
optimizer.optimize_all()
best_solution = optimizer.get_best_solution()
optimizer.visualize_results()
```

### Performance Monitoring

```python
import time
import psutil
import os

def monitor_performance(func, *args, **kwargs):
    """Monitor function performance."""
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    result = func(*args, **kwargs)
    
    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Performance Metrics:")
    print(f"  Execution time: {end_time - start_time:.3f} seconds")
    print(f"  Memory usage: {end_memory - start_memory:.1f} MB")
    
    return result

# Usage
solution = monitor_performance(solve_steiner_tree_constrained, graph)
```

This comprehensive guide covers all major aspects of using the IoT network optimization package, from basic usage to advanced techniques and best practices.
