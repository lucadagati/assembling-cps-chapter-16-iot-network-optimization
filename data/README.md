# Data Directory

This directory contains sample data and network configurations for testing and demonstration purposes.

## Contents

### Sample Networks (`sample_networks.py`)

This module provides pre-defined network configurations for testing algorithms and demonstrating capabilities.

#### Available Networks

1. **Simple Test Network** (`create_simple_test_network()`)
   - 5 nodes total
   - 2 weak nodes, 2 mandatory nodes, 1 discretionary node
   - Basic connectivity for algorithm testing
   - Suitable for unit tests and basic demonstrations

2. **Medium Test Network** (`create_medium_test_network()`)
   - 15 nodes total
   - 8 weak nodes, 3 mandatory nodes, 4 discretionary nodes
   - Realistic connectivity patterns
   - Good for performance testing and algorithm comparison

3. **Large Test Network** (`create_large_test_network()`)
   - 30 nodes total
   - 20 weak nodes, 5 mandatory nodes, 5 discretionary nodes
   - Complex connectivity patterns
   - Suitable for scalability testing

4. **Disconnected Network** (`create_disconnected_network()`)
   - 6 nodes total (2 disconnected components)
   - Tests algorithm robustness
   - Useful for edge case testing

5. **Capacity Constrained Network** (`create_capacity_constrained_network()`)
   - 15 nodes total
   - 10 weak nodes, 2 mandatory nodes, 3 discretionary nodes
   - Tight capacity constraints
   - Challenges algorithm optimization

#### Usage

```python
from data.sample_networks import get_sample_networks, print_network_summary

# Get all sample networks
networks = get_sample_networks()

# Print summary of each network
for name, graph in networks.items():
    print_network_summary(graph, name.capitalize())

# Use specific network
simple_network = networks["simple"]
medium_network = networks["medium"]
```

#### Network Properties

Each network includes:
- **Node Types**: Weak, mandatory, and discretionary nodes
- **Capacity Constraints**: Realistic capacity limits
- **Computational Power**: Varying computational capabilities
- **Edge Weights**: Realistic communication costs
- **Connectivity**: Appropriate connection patterns

## Testing and Validation

### Unit Tests
The sample networks are used in comprehensive unit tests to verify:
- Algorithm correctness
- Edge case handling
- Performance characteristics
- Robustness under different conditions

### Algorithm Validation
Each network is tested with:
- MST algorithms (Kruskal's, Prim's, Constrained)
- Steiner Tree algorithms
- Performance comparison
- Solution quality assessment

### Performance Benchmarking
Networks of different sizes are used to:
- Measure algorithm scalability
- Compare performance across algorithms
- Identify optimization opportunities
- Validate theoretical complexity

## Customization

### Creating Custom Networks
You can create custom networks by modifying the existing functions or creating new ones:

```python
def create_custom_network() -> IoTGraph:
    graph = IoTGraph()
    
    # Add nodes
    for i in range(10):
        node = Node(i, NodeType.WEAK, capacity=1)
        graph.add_node(node)
    
    # Add edges
    for i in range(9):
        edge = Edge(i, i+1, 1.0)
        graph.add_edge(edge)
    
    return graph
```

### Network Parameters
Key parameters you can adjust:
- **Node counts**: Number of nodes by type
- **Capacity constraints**: Maximum connections per node
- **Computational power**: Node processing capabilities
- **Connection probability**: Likelihood of edge existence
- **Weight ranges**: Communication cost distributions

## Integration with Examples

The sample networks are used in the examples directory to demonstrate:
- Algorithm performance
- Network optimization
- Visualization capabilities
- Real-world applications

### Example Usage
```python
# In examples
from data.sample_networks import get_sample_networks

networks = get_sample_networks()
test_network = networks["medium"]

# Run algorithms
from src.algorithms import solve_steiner_tree_constrained
solution = solve_steiner_tree_constrained(test_network)
```

## File Structure

```
data/
├── README.md              # This file
├── sample_networks.py     # Sample network definitions
└── __init__.py           # Package initialization
```

## Dependencies

The sample networks depend on:
- `src.models`: Core graph data structures
- `random`: For generating realistic network properties
- `numpy`: For numerical operations (optional)

## Contributing

To add new sample networks:

1. Create a new function following the naming convention
2. Document the network properties and use cases
3. Add the network to `get_sample_networks()`
4. Update this README with network description
5. Add tests for the new network
6. Verify integration with examples

## References

- Chapter 16: "IoT-driven peer-to-peer networking"
- Graph theory and network optimization literature
- IoT network design principles
- Algorithm testing methodologies
