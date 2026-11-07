"""
Graph generation utilities for creating test IoT networks.

This module provides functions to generate synthetic IoT networks
for testing and demonstration purposes.
"""

import random
import numpy as np
from typing import List, Tuple, Optional, Dict
from ..models import IoTGraph, Node, Edge, NodeType


class GraphGenerator:
    """Utility class for generating synthetic IoT networks."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the graph generator with optional random seed."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
    def generate_random_iot_network(self, 
                                  num_weak: int = 5,
                                  num_mandatory: int = 3,
                                  num_discretionary: int = 2,
                                  connection_probability: float = 0.3,
                                  weight_range: Tuple[float, float] = (1.0, 10.0),
                                  capacity_range: Tuple[int, int] = (2, 5)) -> IoTGraph:
        """
        Generate a random IoT network with specified parameters.
        
        Args:
            num_weak: Number of weak nodes
            num_mandatory: Number of mandatory nodes
            num_discretionary: Number of discretionary nodes
            connection_probability: Probability of edge existence between nodes
            weight_range: Range for edge weights
            capacity_range: Range for node capacities
            
        Returns:
            Generated IoTGraph
        """
        graph = IoTGraph()
        node_id = 0
        
        # Generate weak nodes
        for i in range(num_weak):
            node = Node(
                id=node_id,
                node_type=NodeType.WEAK,
                capacity=1,  # Weak nodes can only connect to one other node
                computational_power=random.uniform(0.7, 1.0)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate mandatory nodes
        for i in range(num_mandatory):
            capacity = random.randint(*capacity_range)
            node = Node(
                id=node_id,
                node_type=NodeType.MANDATORY,
                capacity=capacity,
                computational_power=random.uniform(0.1, 0.4)  # Higher computational power
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate discretionary nodes
        for i in range(num_discretionary):
            capacity = random.randint(*capacity_range)
            node = Node(
                id=node_id,
                node_type=NodeType.DISCRETIONARY,
                capacity=capacity,
                computational_power=random.uniform(0.3, 0.6)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate edges
        all_nodes = list(graph.nodes.keys())
        for i in range(len(all_nodes)):
            for j in range(i + 1, len(all_nodes)):
                if random.random() < connection_probability:
                    weight = random.uniform(*weight_range)
                    edge = Edge(
                        source=all_nodes[i],
                        target=all_nodes[j],
                        weight=weight
                    )
                    graph.add_edge(edge)
        
        self._ensure_connected(graph, weight_range)
        return graph
    
    def _ensure_connected(self, graph: IoTGraph, weight_range: Tuple[float, float]) -> None:
        """Link the connected components of ``graph`` so the network is connected.
        
        Components are bridged through non-weak nodes (weak nodes have capacity 1
        and cannot act as relays); a weak-only component is attached to the
        component of the first non-weak node.
        """
        components, seen = [], set()
        for start in graph.nodes:
            if start in seen:
                continue
            comp = set()
            graph._dfs(start, comp)
            seen |= comp
            components.append(comp)
        if len(components) < 2:
            return
        
        def pick(comp):
            relays = [n for n in comp if graph.nodes[n].node_type != NodeType.WEAK]
            return random.choice(sorted(relays or comp))
        
        anchor = pick(components[0])
        for comp in components[1:]:
            graph.add_edge(Edge(source=anchor, target=pick(comp),
                                weight=random.uniform(*weight_range)))
    
    def generate_grid_iot_network(self, 
                                grid_size: int = 4,
                                num_mandatory: int = 2,
                                num_discretionary: int = 2,
                                weight_base: float = 1.0) -> IoTGraph:
        """
        Generate an IoT network on a grid layout.
        
        Args:
            grid_size: Size of the grid (grid_size x grid_size)
            num_mandatory: Number of mandatory nodes
            num_discretionary: Number of discretionary nodes
            weight_base: Base weight for distance-based edges
            
        Returns:
            Generated IoTGraph with grid layout
        """
        graph = IoTGraph()
        node_id = 0
        
        # Generate weak nodes on grid
        weak_nodes = []
        for i in range(grid_size):
            for j in range(grid_size):
                node = Node(
                    id=node_id,
                    node_type=NodeType.WEAK,
                    capacity=1,
                    computational_power=random.uniform(0.7, 1.0),
                    position=(i, j)
                )
                graph.add_node(node)
                weak_nodes.append(node_id)
                node_id += 1
        
        # Generate mandatory nodes at strategic positions
        mandatory_positions = [(0, 0), (grid_size-1, grid_size-1)]
        for i, (x, y) in enumerate(mandatory_positions[:num_mandatory]):
            node = Node(
                id=node_id,
                node_type=NodeType.MANDATORY,
                capacity=5,
                computational_power=random.uniform(0.1, 0.3),
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate discretionary nodes at random positions
        discretionary_positions = []
        for _ in range(num_discretionary):
            x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
            while (x, y) in discretionary_positions:
                x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
            discretionary_positions.append((x, y))
            
            node = Node(
                id=node_id,
                node_type=NodeType.DISCRETIONARY,
                capacity=3,
                computational_power=random.uniform(0.4, 0.6),
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate edges based on distance
        all_nodes = list(graph.nodes.values())
        for i, node1 in enumerate(all_nodes):
            for j, node2 in enumerate(all_nodes[i+1:], i+1):
                if node1.position and node2.position:
                    # Calculate Euclidean distance
                    distance = np.sqrt(
                        (node1.position[0] - node2.position[0])**2 + 
                        (node1.position[1] - node2.position[1])**2
                    )
                    
                    # Add edge with weight proportional to distance
                    weight = weight_base * distance
                    edge = Edge(
                        source=node1.id,
                        target=node2.id,
                        weight=weight
                    )
                    graph.add_edge(edge)
        
        return graph
    
    def generate_fire_detection_network(self) -> IoTGraph:
        """
        Generate a realistic fire detection network as described in the chapter.
        
        Returns:
            IoTGraph representing a fire detection system
        """
        graph = IoTGraph()
        node_id = 0
        
        # Generate sensor nodes (weak nodes) distributed across territory
        sensor_positions = [
            (0, 0), (2, 0), (4, 0), (6, 0), (8, 0),
            (0, 2), (2, 2), (4, 2), (6, 2), (8, 2),
            (0, 4), (2, 4), (4, 4), (6, 4), (8, 4),
            (0, 6), (2, 6), (4, 6), (6, 6), (8, 6)
        ]
        
        for x, y in sensor_positions:
            node = Node(
                id=node_id,
                node_type=NodeType.WEAK,
                capacity=1,
                computational_power=0.8,  # Limited computational power
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate supply nodes (mandatory nodes) for drone operations
        supply_positions = [(1, 1), (7, 5)]
        for x, y in supply_positions:
            node = Node(
                id=node_id,
                node_type=NodeType.MANDATORY,
                capacity=8,  # High capacity for supply operations
                computational_power=0.2,  # High computational power
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate communication hubs (discretionary nodes)
        hub_positions = [(3, 3), (5, 3)]
        for x, y in hub_positions:
            node = Node(
                id=node_id,
                node_type=NodeType.DISCRETIONARY,
                capacity=4,
                computational_power=0.5,
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate edges based on communication range and cost
        all_nodes = list(graph.nodes.values())
        for i, node1 in enumerate(all_nodes):
            for j, node2 in enumerate(all_nodes[i+1:], i+1):
                if node1.position and node2.position:
                    # Calculate distance
                    distance = np.sqrt(
                        (node1.position[0] - node2.position[0])**2 + 
                        (node1.position[1] - node2.position[1])**2
                    )
                    
                    # Communication range limit
                    max_range = 4.0
                    if distance <= max_range:
                        # Weight based on distance and node types
                        base_weight = distance
                        
                        # Adjust weight based on node types
                        if node1.node_type == NodeType.WEAK and node2.node_type == NodeType.MANDATORY:
                            weight = base_weight * 0.8  # Prefer direct connections
                        elif node1.node_type == NodeType.MANDATORY and node2.node_type == NodeType.MANDATORY:
                            weight = base_weight * 1.2  # Higher cost for mandatory-to-mandatory
                        else:
                            weight = base_weight
                        
                        edge = Edge(
                            source=node1.id,
                            target=node2.id,
                            weight=weight
                        )
                        graph.add_edge(edge)
        
        return graph
    
    def generate_drone_network(self) -> IoTGraph:
        """
        Generate a drone network for UAV operations.
        
        Returns:
            IoTGraph representing a drone coordination network
        """
        graph = IoTGraph()
        node_id = 0
        
        # Generate drone nodes (weak nodes) - limited communication capability
        drone_positions = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1),
            (0, 2), (1, 2), (2, 2), (3, 2)
        ]
        
        for x, y in drone_positions:
            node = Node(
                id=node_id,
                node_type=NodeType.WEAK,
                capacity=1,
                computational_power=0.9,  # Very limited computational power
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate ground control stations (mandatory nodes)
        control_positions = [(0.5, 0.5), (2.5, 1.5)]
        for x, y in control_positions:
            node = Node(
                id=node_id,
                node_type=NodeType.MANDATORY,
                capacity=6,  # Can handle multiple drones
                computational_power=0.1,  # High computational power
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate relay stations (discretionary nodes)
        relay_positions = [(1.5, 0.5), (1.5, 1.5)]
        for x, y in relay_positions:
            node = Node(
                id=node_id,
                node_type=NodeType.DISCRETIONARY,
                capacity=3,
                computational_power=0.4,
                position=(x, y)
            )
            graph.add_node(node)
            node_id += 1
        
        # Generate edges with UAV-specific constraints
        all_nodes = list(graph.nodes.values())
        for i, node1 in enumerate(all_nodes):
            for j, node2 in enumerate(all_nodes[i+1:], i+1):
                if node1.position and node2.position:
                    distance = np.sqrt(
                        (node1.position[0] - node2.position[0])**2 + 
                        (node1.position[1] - node2.position[1])**2
                    )
                    
                    # UAV communication range
                    max_range = 2.5
                    if distance <= max_range:
                        # Weight based on distance and communication type
                        base_weight = distance
                        
                        # Adjust for UAV communication patterns
                        if (node1.node_type == NodeType.WEAK and 
                            node2.node_type == NodeType.MANDATORY):
                            weight = base_weight * 0.7  # Direct drone-to-control
                        elif (node1.node_type == NodeType.WEAK and 
                              node2.node_type == NodeType.DISCRETIONARY):
                            weight = base_weight * 0.9  # Drone-to-relay
                        else:
                            weight = base_weight
                        
                        edge = Edge(
                            source=node1.id,
                            target=node2.id,
                            weight=weight
                        )
                        graph.add_edge(edge)
        
        return graph


def create_sample_networks() -> Dict[str, IoTGraph]:
    """
    Create a collection of sample IoT networks for testing and demonstration.
    
    Returns:
        Dictionary mapping network names to IoTGraph instances
    """
    generator = GraphGenerator(seed=42)
    
    networks = {
        "small_random": generator.generate_random_iot_network(
            num_weak=3, num_mandatory=2, num_discretionary=1
        ),
        "medium_random": generator.generate_random_iot_network(
            num_weak=8, num_mandatory=3, num_discretionary=2
        ),
        "large_random": generator.generate_random_iot_network(
            num_weak=15, num_mandatory=5, num_discretionary=3
        ),
        "grid_4x4": generator.generate_grid_iot_network(grid_size=4),
        "grid_6x6": generator.generate_grid_iot_network(grid_size=6),
        "fire_detection": generator.generate_fire_detection_network(),
        "drone_network": generator.generate_drone_network()
    }
    
    return networks
