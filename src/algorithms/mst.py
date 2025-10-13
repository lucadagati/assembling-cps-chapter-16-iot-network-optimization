"""
Minimum Spanning Tree (MST) algorithms for IoT networks.

This module implements classical MST algorithms (Prim's and Kruskal's)
as described in the chapter, adapted for IoT network optimization.
"""

from typing import List, Tuple, Set, Dict, Optional
import heapq
from dataclasses import dataclass
from ..models import IoTGraph, Node, Edge, NodeType


@dataclass
class MSTSolution:
    """Represents a minimum spanning tree solution."""
    edges: List[Tuple[int, int]]
    total_cost: float
    algorithm_used: str
    
    def __str__(self) -> str:
        return f"MSTSolution(cost={self.total_cost:.2f}, edges={len(self.edges)}, algorithm={self.algorithm_used})"


class MSTAlgorithm:
    """Base class for MST algorithms."""
    
    def __init__(self, graph: IoTGraph):
        """Initialize with an IoT graph."""
        self.graph = graph
    
    def solve(self) -> MSTSolution:
        """Solve the MST problem. Must be implemented by subclasses."""
        raise NotImplementedError


class KruskalMST(MSTAlgorithm):
    """
    Kruskal's algorithm for finding minimum spanning trees.
    
    This algorithm uses an edge-based approach, sorting all edges by weight
    and adding the lowest-weight edge that doesn't create a cycle iteratively.
    """
    
    def solve(self) -> MSTSolution:
        """
        Find MST using Kruskal's algorithm.
        
        Returns:
            MSTSolution containing the MST edges and total cost.
        """
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
        
        return MSTSolution(
            edges=mst_edges,
            total_cost=total_cost,
            algorithm_used="Kruskal"
        )


class PrimMST(MSTAlgorithm):
    """
    Prim's algorithm for finding minimum spanning trees.
    
    This algorithm uses a node-based approach, growing a single tree
    from a starting node by repeatedly adding the minimum-weight edge
    that connects the tree to a new node.
    """
    
    def __init__(self, graph: IoTGraph, start_node: Optional[int] = None):
        """
        Initialize Prim's algorithm.
        
        Args:
            graph: The IoT graph
            start_node: Starting node for the algorithm. If None, uses first node.
        """
        super().__init__(graph)
        self.start_node = start_node or next(iter(graph.nodes.keys()))
    
    def solve(self) -> MSTSolution:
        """
        Find MST using Prim's algorithm.
        
        Returns:
            MSTSolution containing the MST edges and total cost.
        """
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
        
        return MSTSolution(
            edges=mst_edges,
            total_cost=total_cost,
            algorithm_used="Prim"
        )


class ConstrainedMST(MSTAlgorithm):
    """
    MST algorithm with degree constraints for IoT networks.
    
    This implementation addresses the Degree Constrained Minimum Spanning Tree (DCMST)
    problem, which limits the maximum number of connections per node.
    """
    
    def __init__(self, graph: IoTGraph, max_degree: Optional[int] = None):
        """
        Initialize constrained MST algorithm.
        
        Args:
            graph: The IoT graph
            max_degree: Maximum degree for each node. If None, uses node capacity.
        """
        super().__init__(graph)
        self.max_degree = max_degree
    
    def solve(self) -> MSTSolution:
        """
        Find MST with degree constraints using a modified Prim's algorithm.
        
        Returns:
            MSTSolution containing the constrained MST edges and total cost.
        """
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
        
        return MSTSolution(
            edges=mst_edges,
            total_cost=total_cost,
            algorithm_used="ConstrainedPrim"
        )
    
    def _get_max_degree(self, node_id: int) -> int:
        """Get the maximum allowed degree for a node."""
        if self.max_degree is not None:
            return self.max_degree
        
        node = self.graph.nodes[node_id]
        if node.capacity is not None:
            return node.capacity
        
        # Default capacity based on node type
        if node.node_type == NodeType.WEAK:
            return 1
        elif node.node_type == NodeType.MANDATORY:
            return 5  # Default capacity for mandatory nodes
        else:  # DISCRETIONARY
            return 3  # Default capacity for discretionary nodes


def compare_mst_algorithms(graph: IoTGraph) -> Dict[str, MSTSolution]:
    """
    Compare different MST algorithms on the same graph.
    
    Args:
        graph: The IoT graph to analyze
        
    Returns:
        Dictionary mapping algorithm names to their solutions
    """
    algorithms = {
        "Kruskal": KruskalMST(graph),
        "Prim": PrimMST(graph),
        "ConstrainedPrim": ConstrainedMST(graph)
    }
    
    results = {}
    for name, algorithm in algorithms.items():
        try:
            results[name] = algorithm.solve()
        except Exception as e:
            print(f"Error running {name}: {e}")
            results[name] = MSTSolution(edges=[], total_cost=float('inf'), algorithm_used=name)
    
    return results
