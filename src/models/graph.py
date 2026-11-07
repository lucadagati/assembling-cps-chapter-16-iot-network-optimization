"""
Graph data structures and models for IoT network optimization.

This module contains the core data structures used to represent
IoT networks as graphs with different node types and capacity constraints.
"""

from typing import Dict, List, Set, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class NodeType(Enum):
    """Enumeration of node types in the IoT network."""
    WEAK = "weak"           # Must be connected to other devices
    MANDATORY = "mandatory"  # Always included, act as intermediaries
    DISCRETIONARY = "discretionary"  # Optional, included at user's discretion


@dataclass
class Node:
    """Represents a node in the IoT network graph."""
    id: int
    node_type: NodeType
    capacity: Optional[int] = None  # Maximum number of connections
    computational_power: float = 1.0  # Inverse of computational capacity (p_i)
    position: Optional[Tuple[float, float]] = None  # For visualization
    
    def __post_init__(self):
        """Validate node configuration after initialization."""
        if self.node_type == NodeType.MANDATORY and self.capacity is None:
            raise ValueError("Mandatory nodes must have a capacity specified")
        
        # Ensure computational power is in valid range [0.1, 1.0]
        self.computational_power = max(0.1, min(1.0, self.computational_power))


@dataclass
class Edge:
    """Represents an edge in the IoT network graph."""
    source: int
    target: int
    weight: float  # Communication cost (latency, distance, etc.)
    
    def __post_init__(self):
        """Validate edge configuration after initialization."""
        if self.weight < 0:
            raise ValueError("Edge weights must be non-negative")


class IoTGraph:
    """
    Represents an IoT network as a weighted undirected graph.
    
    This class encapsulates the graph structure with support for different
    node types and capacity constraints as described in the chapter.
    """
    
    def __init__(self):
        """Initialize an empty IoT graph."""
        self.nodes: Dict[int, Node] = {}
        self.edges: Dict[Tuple[int, int], Edge] = {}
        self.adjacency_list: Dict[int, Set[int]] = {}
    
    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        self.adjacency_list[node.id] = set()
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        # Add edge in both directions for undirected graph
        self.edges[(edge.source, edge.target)] = edge
        self.edges[(edge.target, edge.source)] = edge
        
        # Update adjacency lists
        self.adjacency_list[edge.source].add(edge.target)
        self.adjacency_list[edge.target].add(edge.source)
    
    def get_neighbors(self, node_id: int) -> Set[int]:
        """Get the set of neighbors for a given node."""
        return self.adjacency_list.get(node_id, set())
    
    def get_edge_weight(self, source: int, target: int) -> Optional[float]:
        """Get the weight of an edge between two nodes."""
        return self.edges.get((source, target), {}).weight if (source, target) in self.edges else None
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        """Get all nodes of a specific type."""
        return [node for node in self.nodes.values() if node.node_type == node_type]
    
    def is_connected(self) -> bool:
        """Check if the graph is connected using DFS."""
        if not self.nodes:
            return True
        
        visited = set()
        start_node = next(iter(self.nodes.keys()))
        self._dfs(start_node, visited)
        
        return len(visited) == len(self.nodes)
    
    def _dfs(self, node_id: int, visited: Set[int]) -> None:
        """Depth-first search helper for connectivity check."""
        visited.add(node_id)
        for neighbor in self.adjacency_list[node_id]:
            if neighbor not in visited:
                self._dfs(neighbor, visited)
    
    def get_shortest_path(self, source: int, target: int) -> Optional[List[int]]:
        """
        Find the shortest path between two nodes using Dijkstra's algorithm.
        
        Returns:
            List of node IDs representing the shortest path, or None if no path exists.
        """
        if source not in self.nodes or target not in self.nodes:
            return None
        
        # Dijkstra's algorithm
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[source] = 0
        previous = {}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            unvisited.remove(current)
            
            if distances[current] == float('inf'):
                break
            
            for neighbor in self.adjacency_list[current]:
                edge_weight = self.get_edge_weight(current, neighbor)
                if edge_weight is not None:
                    alt_distance = distances[current] + edge_weight
                    if alt_distance < distances[neighbor]:
                        distances[neighbor] = alt_distance
                        previous[neighbor] = current
        
        # Reconstruct path
        if distances[target] == float('inf'):
            return None
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return path[::-1]
    
    def get_path_cost(self, path: List[int]) -> float:
        """Calculate the total cost of a path."""
        if len(path) < 2:
            return 0.0
        
        total_cost = 0.0
        for i in range(len(path) - 1):
            weight = self.get_edge_weight(path[i], path[i + 1])
            if weight is not None:
                total_cost += weight
            else:
                return float('inf')  # Invalid path
        
        return total_cost
    
    def to_networkx(self):
        """Convert to NetworkX graph for visualization and analysis."""
        import networkx as nx
        
        G = nx.Graph()
        
        # Add nodes with attributes
        for node in self.nodes.values():
            G.add_node(node.id, 
                      node_type=node.node_type.value,
                      capacity=node.capacity,
                      computational_power=node.computational_power,
                      position=node.position)
        
        # Add edges with weights
        for (u, v), edge in self.edges.items():
            if u < v:  # edges are stored in both directions: add each once
                G.add_edge(u, v, weight=edge.weight)
        
        return G
    
    def __str__(self) -> str:
        """String representation of the graph."""
        return f"IoTGraph(nodes={len(self.nodes)}, edges={len(self.edges)//2})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the graph."""
        return (f"IoTGraph(nodes={len(self.nodes)}, edges={len(self.edges)//2}, "
                f"weak={len(self.get_nodes_by_type(NodeType.WEAK))}, "
                f"mandatory={len(self.get_nodes_by_type(NodeType.MANDATORY))}, "
                f"discretionary={len(self.get_nodes_by_type(NodeType.DISCRETIONARY))})")
