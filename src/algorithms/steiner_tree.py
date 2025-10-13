"""
Steiner Tree algorithms for IoT networks with capacity constraints.

This module implements the constrained Steiner Tree algorithm described in the chapter,
which extends the classical Steiner Tree problem to handle heterogeneous devices
with capacity limitations.
"""

from typing import List, Tuple, Set, Dict, Optional, NamedTuple
from dataclasses import dataclass
import heapq
from ..models import IoTGraph, Node, NodeType


@dataclass
class Path:
    """Represents a path between nodes."""
    nodes: List[int]
    cost: float
    
    def __str__(self) -> str:
        return f"Path({' -> '.join(map(str, self.nodes))}, cost={self.cost:.2f})"


@dataclass
class ConnectionOption:
    """Represents a connection option for a weak node."""
    weak_node: int
    path: Path
    cost: float
    
    def __str__(self) -> str:
        return f"ConnectionOption(node={self.weak_node}, {self.path})"


@dataclass
class SteinerSolution:
    """Represents a Steiner Tree solution."""
    connected_nodes: Set[int]
    edges: List[Tuple[int, int]]
    total_cost: float
    capacity_violations: int
    unconnected_weak_nodes: List[int]
    used_discretionary_nodes: Set[int]
    
    def get_score(self, alpha: float = 0.5) -> float:
        """
        Calculate the objective function score as defined in the chapter.
        
        Args:
            alpha: Weight parameter balancing ACC and AOC components
            
        Returns:
            The objective function value
        """
        n = len(self.connected_nodes)
        if n == 0:
            return float('inf')
        
        # ACC (Average Connection Cost) component
        acc = self.total_cost / (n * (n - 1)) if n > 1 else 0
        
        # AOC (Average Operation Cost) component
        aoc = sum(
            self.graph.nodes[node_id].computational_power * 
            len(self.graph.get_neighbors(node_id))
            for node_id in self.connected_nodes
        ) / n
        
        return alpha * acc + (1 - alpha) * aoc
    
    def __str__(self) -> str:
        return (f"SteinerSolution(cost={self.total_cost:.2f}, "
                f"nodes={len(self.connected_nodes)}, "
                f"violations={self.capacity_violations}, "
                f"unconnected={len(self.unconnected_weak_nodes)})")


class SteinerTreeAlgorithm:
    """Base class for Steiner Tree algorithms."""
    
    def __init__(self, graph: IoTGraph):
        """Initialize with an IoT graph."""
        self.graph = graph
    
    def solve(self, discretionary_nodes: Optional[List[int]] = None) -> SteinerSolution:
        """Solve the Steiner Tree problem. Must be implemented by subclasses."""
        raise NotImplementedError


class GreedySteinerTree(SteinerTreeAlgorithm):
    """
    Greedy algorithm for constrained Steiner Tree problem.
    
    This implementation follows the algorithm described in the chapter,
    using a greedy strategy to connect weak nodes to mandatory nodes
    through optimal paths that may include discretionary nodes.
    """
    
    def __init__(self, graph: IoTGraph):
        """Initialize the greedy Steiner Tree algorithm."""
        super().__init__(graph)
        self.weak_nodes = self.graph.get_nodes_by_type(NodeType.WEAK)
        self.mandatory_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        self.discretionary_nodes = self.graph.get_nodes_by_type(NodeType.DISCRETIONARY)
    
    def solve(self, discretionary_nodes: Optional[List[int]] = None) -> SteinerSolution:
        """
        Solve the Steiner Tree problem using greedy approach.
        
        Args:
            discretionary_nodes: List of discretionary node IDs to include.
                                If None, tests both with and without discretionary nodes.
        
        Returns:
            SteinerSolution containing the optimal solution
        """
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
    
    def _solve_with_discretionary(self, discretionary_node_ids: List[int]) -> SteinerSolution:
        """
        Solve with a specific set of discretionary nodes.
        
        Args:
            discretionary_node_ids: List of discretionary node IDs to include
            
        Returns:
            SteinerSolution for the given discretionary node set
        """
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
    
    def _find_all_paths(self, discretionary_node_ids: List[int]) -> Dict[int, List[Path]]:
        """
        Find all possible paths from weak nodes to mandatory nodes.
        
        Args:
            discretionary_node_ids: List of discretionary node IDs to consider
            
        Returns:
            Dictionary mapping weak node IDs to lists of possible paths
        """
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
    
    def _can_connect_path(self, path: Path, capacity_usage: Dict[int, int], 
                         connected_nodes: Set[int]) -> bool:
        """Check if a path can be connected without violating capacity constraints."""
        for i in range(len(path.nodes) - 1):
            node_id = path.nodes[i]
            if node_id in connected_nodes:
                node = self.graph.nodes[node_id]
                if node.capacity is not None and capacity_usage[node_id] >= node.capacity:
                    return False
        return True
    
    def _connect_path(self, path: Path, connected_nodes: Set[int], 
                     steiner_edges: List[Tuple[int, int]], 
                     capacity_usage: Dict[int, int]) -> None:
        """Connect a path and update the solution state."""
        # Add all nodes in the path
        for node_id in path.nodes:
            connected_nodes.add(node_id)
        
        # Add all edges in the path
        for i in range(len(path.nodes) - 1):
            edge = (path.nodes[i], path.nodes[i + 1])
            if edge not in steiner_edges and (edge[1], edge[0]) not in steiner_edges:
                steiner_edges.append(edge)
                capacity_usage[edge[0]] += 1
                capacity_usage[edge[1]] += 1
    
    def _find_cheapest_path(self, weak_node_id: int, 
                          discretionary_node_ids: List[int]) -> Optional[Path]:
        """Find the cheapest path for a weak node."""
        all_paths = self._find_all_paths(discretionary_node_ids)
        if weak_node_id in all_paths and all_paths[weak_node_id]:
            return all_paths[weak_node_id][0]  # Already sorted by cost
        return None
    
    def _count_capacity_violations(self, capacity_usage: Dict[int, int]) -> int:
        """Count the number of capacity constraint violations."""
        violations = 0
        for node_id, usage in capacity_usage.items():
            node = self.graph.nodes[node_id]
            if node.capacity is not None and usage > node.capacity:
                violations += 1
        return violations


def solve_steiner_tree_constrained(graph: IoTGraph) -> SteinerSolution:
    """
    Main function to solve the constrained Steiner Tree problem.
    
    This function implements the algorithm described in the chapter:
    1. Test solution without discretionary nodes
    2. Test solution with all discretionary nodes
    3. Return the best solution
    
    Args:
        graph: The IoT graph to solve
        
    Returns:
        SteinerSolution containing the optimal solution
    """
    algorithm = GreedySteinerTree(graph)
    
    # Test solution without discretionary nodes
    solution_without = algorithm.solve([])
    
    # Test solution with all discretionary nodes
    all_discretionary = [n.id for n in algorithm.discretionary_nodes]
    solution_with_all = algorithm.solve(all_discretionary)
    
    # Return the better solution
    if solution_without.get_score() <= solution_with_all.get_score():
        return solution_without
    else:
        return solution_with_all
