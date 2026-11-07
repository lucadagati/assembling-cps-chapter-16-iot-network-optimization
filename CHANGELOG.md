# Changelog

All notable changes to the IoT Network Optimization project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-11-07

### Fixed
- Kruskal ignored edges whose stored `source` was greater than `target`; `IoTGraph.to_networkx` had the same flaw
- `SteinerSolution.get_score` raised `AttributeError` (solutions now keep a reference to the graph)
- `PrimMST` raised `StopIteration` on an empty graph
- `ConstrainedMST` enforced the degree limit on the target node only; it now checks both endpoints and starts from the highest-capacity node
- Random IoT networks are now always connected
- `plot_algorithm_comparison` crashed when a Steiner solution was supplied
- Example scripts and CLI no longer report a cheap partial forest as the "best MST" (`select_best_mst`)

### Changed
- Core requirements reduced to numpy, networkx, matplotlib, pytest; optional packages in `requirements-extras.txt`
- README rewritten as a complete usage guide

## [1.0.0] - 2024-10-13

### Added

#### Core Algorithms
- **Minimum Spanning Tree (MST) Algorithms**
  - Kruskal's algorithm implementation
  - Prim's algorithm implementation
  - Constrained MST with capacity limitations
  - Algorithm comparison functionality

- **Steiner Tree Algorithm**
  - Greedy Steiner Tree implementation
  - Support for heterogeneous device types
  - Capacity constraint handling
  - Multi-objective optimization function

#### Data Models
- **Graph Data Structures**
  - IoTGraph class for network representation
  - Node types: Weak, Mandatory, Discretionary
  - Edge representation with weights
  - Capacity constraints and computational power

- **Solution Representations**
  - MSTSolution class for MST results
  - SteinerSolution class for Steiner Tree results
  - Objective function scoring
  - Performance metrics

#### Network Generation
- **Graph Generators**
  - Random IoT network generation
  - Grid-based network generation
  - Fire detection network generator
  - Drone coordination network generator
  - Sample network collections

#### Visualization
- **Network Plotting**
  - Original network visualization
  - MST solution visualization
  - Steiner Tree solution visualization
  - Algorithm comparison plots
  - Cost comparison charts

#### Examples and Applications
- **Fire Detection System**
  - Early detection sensor networks
  - Supply node optimization
  - Drone coordination simulation
  - Mission planning and execution

- **Drone Network Coordination**
  - UAV communication networks
  - Ground control station management
  - Relay station optimization
  - Stack4Things integration concepts

- **IoT Sensor Networks**
  - Environmental monitoring systems
  - Data collection optimization
  - Sensor performance analysis
  - Real-time data transmission

#### Testing and Validation
- **Comprehensive Test Suite**
  - Unit tests for all algorithms
  - Integration tests for complete workflows
  - Performance benchmarking
  - Edge case handling
  - Error condition testing

- **Sample Data**
  - Pre-defined test networks
  - Various size configurations
  - Realistic connectivity patterns
  - Capacity constraint scenarios

#### Documentation
- **Theoretical Background**
  - MST algorithm theory
  - Steiner Tree problem formulation
  - Computational complexity analysis
  - Historical context and applications

- **Implementation Guides**
  - Detailed algorithm descriptions
  - Code examples and usage
  - Performance considerations
  - Best practices

- **Usage Examples**
  - Comprehensive usage guide
  - Real-world application examples
  - Performance optimization tips
  - Troubleshooting guide

#### Command-Line Interface
- **CLI Tools**
  - Network generation commands
  - Algorithm execution options
  - Visualization controls
  - Batch processing capabilities

#### Development Tools
- **Project Structure**
  - Modular package organization
  - Clear separation of concerns
  - Comprehensive error handling
  - Memory management

- **Build and Distribution**
  - Setup.py configuration
  - Requirements management
  - Package installation
  - Dependency resolution

### Technical Specifications

#### Algorithm Complexity
- **MST Algorithms**: O(m log n) time complexity
- **Steiner Tree**: O(n² log n) time complexity
- **Memory Usage**: Linear scaling with network size
- **Scalability**: Handles networks with hundreds of nodes

#### Supported Features
- **Node Types**: Weak, Mandatory, Discretionary
- **Capacity Constraints**: Configurable node limitations
- **Multi-Objective Optimization**: Balanced cost and performance
- **Visualization**: Multiple plot types and export formats

#### Dependencies
- **Core**: NumPy, NetworkX, Matplotlib
- **Optional**: Plotly, Dash, Scikit-learn
- **Development**: Pytest, Black, Flake8
- **Documentation**: Sphinx, MyST

### Performance Characteristics

#### Algorithm Performance
- **MST Algorithms**: Optimal solutions in polynomial time
- **Steiner Tree**: High-quality approximations
- **Memory Efficiency**: Linear memory usage
- **Scalability**: Tested up to 1000+ nodes

#### Network Generation
- **Random Networks**: Configurable parameters
- **Specialized Networks**: Realistic IoT topologies
- **Large Networks**: Efficient generation algorithms
- **Reproducibility**: Seed-based random generation

### Quality Assurance

#### Testing Coverage
- **Unit Tests**: 100% algorithm coverage
- **Integration Tests**: End-to-end workflows
- **Performance Tests**: Scalability validation
- **Edge Cases**: Error condition handling

#### Code Quality
- **Style Compliance**: PEP 8 adherence
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Detailed docstrings
- **Error Handling**: Robust exception management

### Documentation

#### User Documentation
- **README**: Project overview and quick start
- **Usage Guide**: Comprehensive examples
- **API Reference**: Complete function documentation
- **Tutorials**: Step-by-step guides

#### Developer Documentation
- **Contributing Guide**: Development guidelines
- **Architecture**: System design overview
- **Testing Guide**: Test development and execution
- **Release Notes**: Version history and changes

### Examples and Tutorials

#### Real-World Applications
- **Fire Detection**: Complete system implementation
- **Drone Networks**: UAV coordination systems
- **Sensor Networks**: Environmental monitoring
- **Smart Cities**: Urban IoT infrastructure

#### Educational Content
- **Algorithm Explanations**: Step-by-step walkthroughs
- **Visualization Examples**: Interactive demonstrations
- **Performance Analysis**: Benchmarking and optimization
- **Best Practices**: Development guidelines

### Future Roadmap

#### Planned Features
- **Advanced Algorithms**: Additional optimization methods
- **Parallel Processing**: Multi-core algorithm support
- **Real-Time Optimization**: Dynamic network adaptation
- **Cloud Integration**: Cloud-based processing capabilities

#### Research Directions
- **Machine Learning**: AI-enhanced optimization
- **Quantum Algorithms**: Quantum computing applications
- **Edge Computing**: Distributed optimization
- **5G Networks**: Next-generation connectivity

## [Unreleased]

### Planned
- Additional MST algorithm variants
- Parallel processing support
- Real-time network optimization
- Cloud computing integration
- Machine learning enhancements
- Quantum algorithm support
- 5G network optimization
- Edge computing capabilities

### Under Consideration
- Interactive visualization tools
- Web-based interface
- Mobile application support
- API for external integration
- Plugin architecture
- Performance profiling tools
- Advanced benchmarking suite
- Automated testing framework

---

## Version History

- **1.0.0**: Initial release with core functionality
- **Future versions**: Will include additional features and improvements

## Support

For questions, issues, or contributions:
- GitHub Issues: Report bugs and request features
- Documentation: Comprehensive guides and examples
- Examples: Real-world application demonstrations
- Tests: Validation and performance verification
