# Examples Directory

This directory contains practical examples demonstrating the implementation and usage of the IoT network optimization algorithms described in Chapter 16.

## Available Examples

### 1. Fire Detection System (`fire_detection/`)

**File**: `fire_detection_system.py`

**Description**: Implements the fire detection and intervention system described in the chapter, including:
- Early detection sensors distributed across territory
- Supply nodes for drone operations
- Communication hubs for network optimization
- Drone coordination for fire intervention

**Key Features**:
- Realistic network topology based on geographical distribution
- Capacity constraints for supply nodes
- Mission simulation and performance analysis
- Visualization of network optimization results

**Usage**:
```bash
cd examples/fire_detection
python fire_detection_system.py
```

### 2. Drone Network Coordination (`drone_network/`)

**File**: `drone_coordination.py`

**Description**: Demonstrates drone network coordination using Stack4Things integration, including:
- UAV nodes with limited communication capability
- Ground control stations as mandatory nodes
- Relay stations as discretionary nodes
- Mission planning and execution simulation

**Key Features**:
- Stack4Things framework integration concepts
- Drone mission simulation
- Network performance analysis
- Cloud-based resource management

**Usage**:
```bash
cd examples/drone_network
python drone_coordination.py
```

### 3. IoT Sensor Network (`iot_sensors/`)

**File**: `sensor_network.py`

**Description**: Implements an IoT sensor network for environmental monitoring, including:
- Sensor nodes for data collection
- Data collection hubs as mandatory nodes
- Relay nodes for network optimization
- Environmental monitoring simulation

**Key Features**:
- Data collection simulation
- Sensor performance analysis
- Network efficiency metrics
- Environmental monitoring capabilities

**Usage**:
```bash
cd examples/iot_sensors
python sensor_network.py
```

## Common Features

All examples include:

### Network Optimization
- **Constrained Steiner Tree**: Solves the heterogeneous device connectivity problem
- **MST Algorithms**: Compares Kruskal's, Prim's, and constrained MST algorithms
- **Performance Analysis**: Evaluates algorithm effectiveness and efficiency

### Visualization
- **Network Topology**: Shows original network structure
- **Solution Visualization**: Displays optimized network connections
- **Algorithm Comparison**: Compares different optimization approaches
- **Cost Analysis**: Bar charts showing algorithm performance

### Simulation Capabilities
- **Realistic Scenarios**: Based on real-world IoT applications
- **Performance Metrics**: Connectivity, capacity utilization, efficiency
- **Mission Simulation**: Task execution and resource management
- **Data Collection**: Sensor data transmission and analysis

## Running Examples

### Prerequisites
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure you're in the project root directory

### Individual Example Execution
Each example can be run independently:
```bash
python examples/fire_detection/fire_detection_system.py
python examples/drone_network/drone_coordination.py
python examples/iot_sensors/sensor_network.py
```

### Batch Execution
Run all examples sequentially:
```bash
python examples/fire_detection/fire_detection_system.py
python examples/drone_network/drone_coordination.py
python examples/iot_sensors/sensor_network.py
```

## Output Files

Each example generates several output files:

### Visualization Files
- `*_original.png`: Original network topology
- `*_steiner.png`: Steiner Tree solution
- `*_comparison.png`: Algorithm comparison
- `*_costs.png`: Cost comparison chart

### Console Output
- Network creation details
- Optimization results
- Performance analysis
- Simulation results

## Customization

### Network Parameters
You can modify network parameters in each example:
- Number of nodes by type
- Connection probabilities
- Weight ranges
- Capacity constraints

### Simulation Parameters
Adjust simulation settings:
- Number of missions/rounds
- Data collection frequency
- Performance thresholds
- Visualization options

### Algorithm Parameters
Customize algorithm behavior:
- Alpha parameter for objective function
- Capacity constraints
- Path finding strategies
- Optimization criteria

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure you're running from the project root directory
2. **Missing Dependencies**: Install all requirements from `requirements.txt`
3. **Visualization Issues**: Check matplotlib backend configuration
4. **Memory Issues**: Reduce network size for large simulations

### Performance Tips
1. **Network Size**: Start with smaller networks for testing
2. **Visualization**: Disable plot saving for faster execution
3. **Simulation Rounds**: Reduce number of rounds for quick testing
4. **Algorithm Selection**: Use faster algorithms for large networks

## Integration with Main Package

These examples demonstrate how to use the main package components:

### Core Models
```python
from src.models import IoTGraph, Node, Edge, NodeType
```

### Algorithms
```python
from src.algorithms import solve_steiner_tree_constrained, compare_mst_algorithms
```

### Utilities
```python
from src.utils import GraphGenerator, create_sample_networks
```

### Visualization
```python
from src.visualization import NetworkPlotter
```

## Contributing

To add new examples:

1. Create a new directory under `examples/`
2. Implement your example following the existing pattern
3. Include comprehensive documentation
4. Add visualization capabilities
5. Test with different network configurations
6. Update this README with your example details

## References

- Chapter 16: "IoT-driven peer-to-peer networking"
- Stack4Things framework documentation
- IoT network optimization literature
- Environmental monitoring applications
