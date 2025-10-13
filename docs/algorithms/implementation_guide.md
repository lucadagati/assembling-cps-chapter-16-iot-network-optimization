# Algorithm Implementation Guide

## Overview

This guide provides detailed information about the implementation of the algorithms described in Chapter 16, including the Minimum Spanning Tree (MST) algorithms and the constrained Steiner Tree algorithm.

## Minimum Spanning Tree Algorithms

### Kruskal's Algorithm Implementation

#### Core Logic
```python
def solve(self) -> MSTSolution:
    # Get all edges and sort by weight
    edges = []
    for edge in self.graph.edges.values():
        if edge.source < edge.target:  # Avoid duplicates
            edges.append((edge.source, edge.target, edge.weight))
    
    edges.sort(key=lambda x: x[2])  # Sort by weight
    
    # Union-Find data structure for cycle detection
    parent = {node_id: node_id for node_id in self.graph.nodes}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Build MST
    mst_edges = []
    total_cost = 0.0
    
    for source, target, weight in edges:
        if union(source, target):
            mst_edges.append((source, target))
            total_cost += weight
            
            # Stop when we have n-1 edges (tree property)
            if len(mst_edges) == len(self.graph.nodes) - 1:
                break
    
    return MSTSolution(edges=mst_edges, total_cost=total_cost, algorithm_used="Kruskal")
```

#### Key Features
- **Edge-based approach**: Processes edges in order of increasing weight
- **Cycle detection**: Uses Union-Find data structure
- **Time complexity**: O(m log n) where m is edges and n is vertices
- **Space complexity**: O(n) for Union-Find structure

### Prim's Algorithm Implementation

#### Core Logic
```python
def solve(self) -> MSTSolution:
    if not self.graph.nodes:
        return MSTSolution(edges=[], total_cost=0.0, algorithm_used="Prim")
    
    # Priority queue: (weight, source, target)
    heap = []
    visited = {self.start_node}
    mst_edges = []
    total_cost = 0.0
    
    # Add all edges from start node to heap
    for neighbor in self.graph.get_neighbors(self.start_node):
        weight = self.graph.get_edge_weight(self.start_node, neighbor)
        if weight is not None:
            heapq.heappush(heap, (weight, self.start_node, neighbor))
    
    # Grow the tree
    while heap and len(visited) < len(self.graph.nodes):
        weight, source, target = heapq.heappop(heap)
        
        if target not in visited:
            visited.add(target)
            mst_edges.append((source, target))
            total_cost += weight
            
            # Add edges from the new node
            for neighbor in self.graph.get_neighbors(target):
                if neighbor not in visited:
                    edge_weight = self.graph.get_edge_weight(target, neighbor)
                    if edge_weight is not None:
                        heapq.heappush(heap, (edge_weight, target, neighbor))
    
    return MSTSolution(edges=mst_edges, total_cost=total_cost, algorithm_used="Prim")
```

#### Key Features
- **Node-based approach**: Grows tree from a starting node
- **Priority queue**: Uses heap for efficient edge selection
- **Time complexity**: O(m log n) with binary heap
- **Space complexity**: O(n) for visited set and heap

### Constrained MST Implementation

#### Core Logic
```python
def solve(self) -> MSTSolution:
    if not self.graph.nodes:
        return MSTSolution(edges=[], total_cost=0.0, algorithm_used="ConstrainedPrim")
    
    # Initialize degree tracking
    node_degrees = {node_id: 0 for node_id in self.graph.nodes}
    
    # Priority queue: (weight, source, target)
    heap = []
    visited = set()
    mst_edges = []
    total_cost = 0.0
    
    # Start with first node
    start_node = next(iter(self.graph.nodes.keys()))
    visited.add(start_node)
    
    # Add all edges from start node
    for neighbor in self.graph.get_neighbors(start_node):
        weight = self.graph.get_edge_weight(start_node, neighbor)
        if weight is not None:
            heapq.heappush(heap, (weight, start_node, neighbor))
    
    # Grow the tree with degree constraints
    while heap and len(visited) < len(self.graph.nodes):
        weight, source, target = heapq.heappop(heap)
        
        if target not in visited:
            # Check degree constraints
            max_allowed = self._get_max_degree(target)
            if node_degrees[target] < max_allowed:
                visited.add(target)
                mst_edges.append((source, target))
                total_cost += weight
                node_degrees[source] += 1
                node_degrees[target] += 1
                
                # Add edges from the new node
                for neighbor in self.graph.get_neighbors(target):
                    if neighbor not in visited:
                        edge_weight = self.graph.get_edge_weight(target, neighbor)
                        if edge_weight is not None:
                            heapq.heappush(heap, (edge_weight, target, neighbor))
    
    return MSTSolution(edges=mst_edges, total_cost=total_cost, algorithm_used="ConstrainedPrim")
```

#### Key Features
- **Degree constraints**: Limits connections per node
- **Capacity awareness**: Respects node capacity limits
- **Modified Prim's**: Extends Prim's algorithm with constraints
- **Violation tracking**: Monitors constraint violations

## Constrained Steiner Tree Algorithm

### Greedy Algorithm Implementation

#### Main Algorithm Structure
```python
def solve(self, discretionary_nodes: Optional[List[int]] = None) -> SteinerSolution:
    if discretionary_nodes is None:
        # Test both scenarios and return the best
        solution_without = self._solve_with_discretionary([])
        solution_with_all = self._solve_with_discretionary([n.id for n in self.discretionary_nodes])
        
        if solution_without.get_score() <= solution_with_all.get_score():
            return solution_without
        else:
            return solution_with_all
    else:
        return self._solve_with_discretionary(discretionary_nodes)
```

#### Core Solving Logic
```python
def _solve_with_discretionary(self, discretionary_node_ids: List[int]) -> SteinerSolution:
    # Initialize solution state
    capacity_usage = {node_id: 0 for node_id in self.graph.nodes}
    connected_nodes = set()
    steiner_edges = []
    total_cost = 0.0
    
    # Always include mandatory nodes
    for node in self.mandatory_nodes:
        connected_nodes.add(node.id)
    
    # Include selected discretionary nodes
    for node_id in discretionary_node_ids:
        connected_nodes.add(node_id)
    
    # Find all possible paths for weak nodes
    all_paths = self._find_all_paths(discretionary_node_ids)
    
    # Create connection options
    options = []
    for weak_node in self.weak_nodes:
        if weak_node.id in all_paths:
            for path in all_paths[weak_node.id]:
                options.append(ConnectionOption(
                    weak_node=weak_node.id,
                    path=path,
                    cost=path.cost
                ))
    
    # Sort options by cost
    options.sort(key=lambda x: x.cost)
    
    # Greedy algorithm
    for option in options:
        weak_node_id = option.weak_node
        
        # Check if weak node is already connected
        if weak_node_id in connected_nodes:
            continue
        
        # Check capacity constraints
        if self._can_connect_path(option.path, capacity_usage, connected_nodes):
            # Connect the path
            self._connect_path(option.path, connected_nodes, steiner_edges, capacity_usage)
            total_cost += option.cost
    
    # Force connection of remaining weak nodes (even if violates capacity)
    unconnected_weak = []
    for weak_node in self.weak_nodes:
        if weak_node.id not in connected_nodes:
            unconnected_weak.append(weak_node.id)
            # Find cheapest available path
            cheapest_path = self._find_cheapest_path(weak_node.id, discretionary_node_ids)
            if cheapest_path:
                self._connect_path(cheapest_path, connected_nodes, steiner_edges, capacity_usage)
                total_cost += cheapest_path.cost
    
    # Calculate capacity violations
    violations = self._count_capacity_violations(capacity_usage)
    
    return SteinerSolution(
        connected_nodes=connected_nodes,
        edges=steiner_edges,
        total_cost=total_cost,
        capacity_violations=violations,
        unconnected_weak_nodes=unconnected_weak,
        used_discretionary_nodes=set(discretionary_node_ids) & connected_nodes
    )
```

#### Path Finding Logic
```python
def _find_all_paths(self, discretionary_node_ids: List[int]) -> Dict[int, List[Path]]:
    paths = {}
    
    for weak_node in self.weak_nodes:
        weak_id = weak_node.id
        paths[weak_id] = []
        
        # Direct paths to mandatory nodes
        for mandatory_node in self.mandatory_nodes:
            mand_id = mandatory_node.id
            if self.graph.get_edge_weight(weak_id, mand_id) is not None:
                paths[weak_id].append(Path(
                    nodes=[weak_id, mand_id],
                    cost=self.graph.get_edge_weight(weak_id, mand_id)
                ))
        
        # Paths with one discretionary intermediary
        for disc_id in discretionary_node_ids:
            if self.graph.get_edge_weight(weak_id, disc_id) is not None:
                for mandatory_node in self.mandatory_nodes:
                    mand_id = mandatory_node.id
                    if self.graph.get_edge_weight(disc_id, mand_id) is not None:
                        cost = (self.graph.get_edge_weight(weak_id, disc_id) + 
                               self.graph.get_edge_weight(disc_id, mand_id))
                        paths[weak_id].append(Path(
                            nodes=[weak_id, disc_id, mand_id],
                            cost=cost
                        ))
        
        # Paths with two discretionary intermediaries
        for i, disc1_id in enumerate(discretionary_node_ids):
            for disc2_id in discretionary_node_ids[i+1:]:
                if (self.graph.get_edge_weight(weak_id, disc1_id) is not None and
                    self.graph.get_edge_weight(disc1_id, disc2_id) is not None):
                    for mandatory_node in self.mandatory_nodes:
                        mand_id = mandatory_node.id
                        if self.graph.get_edge_weight(disc2_id, mand_id) is not None:
                            cost = (self.graph.get_edge_weight(weak_id, disc1_id) +
                                   self.graph.get_edge_weight(disc1_id, disc2_id) +
                                   self.graph.get_edge_weight(disc2_id, mand_id))
                            paths[weak_id].append(Path(
                                nodes=[weak_id, disc1_id, disc2_id, mand_id],
                                cost=cost
                            ))
        
        # Sort paths by cost
        paths[weak_id].sort(key=lambda p: p.cost)
    
    return paths
```

## Key Implementation Details

### Data Structures

#### Node Representation
```python
@dataclass
class Node:
    id: int
    node_type: NodeType
    capacity: Optional[int] = None
    computational_power: float = 1.0
    position: Optional[Tuple[float, float]] = None
```

#### Edge Representation
```python
@dataclass
class Edge:
    source: int
    target: int
    weight: float
```

#### Path Representation
```python
@dataclass
class Path:
    nodes: List[int]
    cost: float
```

### Algorithm Complexity

#### Time Complexity
- **Kruskal's Algorithm**: O(m log n) - dominated by sorting
- **Prim's Algorithm**: O(m log n) - heap operations
- **Constrained MST**: O(m log n) - same as Prim's with additional checks
- **Steiner Tree**: O(n² log n) - path finding and sorting

#### Space Complexity
- **MST Algorithms**: O(n) - for data structures
- **Steiner Tree**: O(n²) - for storing all possible paths

### Optimization Techniques

#### Path Precomputation
- Calculate all possible paths in advance
- Sort paths by cost for efficient selection
- Cache results to avoid recomputation

#### Capacity Tracking
- Real-time monitoring of node capacity usage
- Efficient constraint violation detection
- Graceful handling of capacity limits

#### Greedy Selection
- Local optimization at each step
- Cost-benefit ratio consideration
- Multi-factor decision making

## Usage Examples

### Basic MST Usage
```python
from src.algorithms import KruskalMST, PrimMST
from src.utils import create_sample_networks

# Create a sample network
networks = create_sample_networks()
graph = networks["medium_random"]

# Solve using Kruskal's algorithm
kruskal = KruskalMST(graph)
solution = kruskal.solve()
print(f"Kruskal MST cost: {solution.total_cost:.2f}")

# Solve using Prim's algorithm
prim = PrimMST(graph)
solution = prim.solve()
print(f"Prim MST cost: {solution.total_cost:.2f}")
```

### Constrained Steiner Tree Usage
```python
from src.algorithms import solve_steiner_tree_constrained
from src.utils import create_sample_networks

# Create a sample network
networks = create_sample_networks()
graph = networks["fire_detection"]

# Solve the constrained Steiner Tree problem
solution = solve_steiner_tree_constrained(graph)
print(f"Steiner Tree cost: {solution.total_cost:.2f}")
print(f"Capacity violations: {solution.capacity_violations}")
print(f"Unconnected weak nodes: {len(solution.unconnected_weak_nodes)}")
```

### Algorithm Comparison
```python
from src.algorithms import compare_mst_algorithms
from src.utils import create_sample_networks

# Create a sample network
networks = create_sample_networks()
graph = networks["large_random"]

# Compare different MST algorithms
results = compare_mst_algorithms(graph)
for name, solution in results.items():
    print(f"{name}: {solution}")
```

## Performance Considerations

### Scalability
- Algorithms handle networks with hundreds of nodes efficiently
- Memory usage scales linearly with network size
- Consider parallel processing for very large networks

### Optimization Opportunities
- Use more efficient data structures for large graphs
- Implement parallel path finding for Steiner Tree
- Cache frequently accessed graph properties

### Error Handling
- Validate input graphs for connectivity
- Handle edge cases (empty graphs, single nodes)
- Provide meaningful error messages

## Testing and Validation

### Unit Tests
- Test individual algorithm components
- Verify correctness on known examples
- Check edge cases and error conditions

### Integration Tests
- Test complete algorithm workflows
- Validate results against expected outcomes
- Performance benchmarking

### Visualization
- Use network visualization to verify results
- Compare algorithm outputs visually
- Debug connectivity and constraint issues
