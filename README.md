# IoT Network Optimization Algorithms

## Overview

This repository implements algorithms for optimizing IoT network connectivity problems, including Minimum Spanning Tree (MST) algorithms and constrained Steiner Tree algorithms for heterogeneous device networks.

The implementation is based on research presented in Chapter 16 of "Assembling Smart Cyber-Physical Systems: heterogeneous, diffuse and green technological infrastructures for cities and industries".

## Problem Statement

Internet of Things (IoT) networks consist of interconnected devices that communicate with each other autonomously. Device communication is often done with the aim of minimizing communication costs while maintaining full connectivity.

The standard approach to ensuring full network connectivity is based on **minimum spanning tree** (MST) algorithms. However, real-world constraints, such as node capacity limits and device heterogeneity, can result in an unsatisfactory outcome of MST algorithms.

This implementation presents a realistic problem solved by leveraging IoT orchestration frameworks. Our model considers three types of devices:
- **Weak devices**: must be connected to other devices
- **Mandatory devices**: always included and act as intermediaries among devices
- **Discretionary devices**: included at user's discretion to reduce latency or balance load

## Repository Structure

```
chapter16/
├── README.md                 # This file
├── docs/                     # Documentation
│   ├── theory/              # Theoretical background
│   ├── algorithms/          # Algorithm descriptions
│   └── examples/            # Usage examples
├── src/                     # Source code
│   ├── algorithms/          # Algorithm implementations
│   ├── models/              # Data models and structures
│   ├── utils/               # Utility functions
│   └── visualization/       # Visualization tools
├── examples/                # Practical examples
│   ├── fire_detection/      # Fire detection system example
│   ├── drone_network/       # Drone network example
│   └── iot_sensors/         # IoT sensor network example
├── tests/                   # Unit tests
├── data/                    # Sample data and graphs
└── requirements.txt         # Python dependencies
```

## Key Features

1. **Heterogeneous Device Model**: Support for different device types with varying capabilities and constraints
2. **Multi-Objective Optimization**: Objective function that balances edge costs, connectivity penalties, and capacity constraints
3. **Practical Implementation**: Real-world applications including fire detection systems and drone coordination

## Algorithms Implemented

- **Minimum Spanning Tree (MST)**: Classical algorithms (Prim's, Kruskal's)
- **Steiner Tree**: Constrained Steiner tree with capacity limitations
- **Greedy Algorithm**: Advanced greedy strategy for IoT network optimization

## Applications

- Environmental monitoring systems
- Fire detection and intervention systems
- Drone network coordination
- Smart city infrastructure
- Industrial IoT networks

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd chapter16

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from src.algorithms import solve_steiner_tree_constrained, compare_mst_algorithms
from src.utils import GraphGenerator

# Create a network
generator = GraphGenerator(seed=42)
graph = generator.generate_random_iot_network(num_weak=10, num_mandatory=3, num_discretionary=2)

# Solve optimization problem
solution = solve_steiner_tree_constrained(graph)
print(f"Total cost: {solution.total_cost:.2f}")

# Compare MST algorithms
mst_results = compare_mst_algorithms(graph)
for name, result in mst_results.items():
    print(f"{name}: {result.total_cost:.2f}")
```

See the `examples/` directory for complete usage examples and the `docs/` directory for detailed documentation.

## Testing

```bash
# Run all tests
python run_tests.py

# Run examples
python run_examples.py
```

## License

MIT License - see LICENSE file for details.

## Citation

If you use this code in your research, please cite:

```
Chapter 16: IoT-driven peer-to-peer networking
In: "Assembling Smart Cyber-Physical Systems: heterogeneous, diffuse and green technological infrastructures for cities and industries"
Authors: Prof. Giuseppe Tricomi, Prof. Pasquale De Meo, Dr. Marco Garofalo
```
