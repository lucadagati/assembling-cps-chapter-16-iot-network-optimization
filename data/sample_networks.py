"""
Sample network data for testing and demonstration.

This module provides pre-defined network configurations
for testing algorithms and demonstrating capabilities.
"""

from src.models import IoTGraph, Node, Edge, NodeType


def create_simple_test_network() -> IoTGraph:
    """
    Create a simple test network for basic algorithm testing.
    
    Returns:
        IoTGraph: Simple test network with 5 nodes
    """
    graph = IoTGraph()
    
    # Add nodes
    nodes = [
        Node(0, NodeType.WEAK, capacity=1, computational_power=0.8),
        Node(1, NodeType.WEAK, capacity=1, computational_power=0.9),
        Node(2, NodeType.MANDATORY, capacity=3, computational_power=0.2),
        Node(3, NodeType.MANDATORY, capacity=4, computational_power=0.3),
        Node(4, NodeType.DISCRETIONARY, capacity=2, computational_power=0.5)
    ]
    
    for node in nodes:
        graph.add_node(node)
    
    # Add edges
    edges = [
        Edge(0, 2, 5.0),
        Edge(0, 4, 3.0),
        Edge(1, 3, 4.0),
        Edge(1, 4, 2.0),
        Edge(2, 3, 6.0),
        Edge(2, 4, 2.0),
        Edge(3, 4, 3.0)
    ]
    
    for edge in edges:
        graph.add_edge(edge)
    
    return graph


def create_medium_test_network() -> IoTGraph:
    """
    Create a medium-sized test network for performance testing.
    
    Returns:
        IoTGraph: Medium test network with 15 nodes
    """
    graph = IoTGraph()
    
    # Add weak nodes (sensors)
    for i in range(8):
        node = Node(i, NodeType.WEAK, capacity=1, computational_power=0.8)
        graph.add_node(node)
    
    # Add mandatory nodes (hubs)
    for i in range(8, 11):
        node = Node(i, NodeType.MANDATORY, capacity=5, computational_power=0.2)
        graph.add_node(node)
    
    # Add discretionary nodes (relays)
    for i in range(11, 15):
        node = Node(i, NodeType.DISCRETIONARY, capacity=3, computational_power=0.5)
        graph.add_node(node)
    
    # Add edges with realistic weights
    import random
    random.seed(42)
    
    # Connect weak nodes to mandatory nodes
    for weak_id in range(8):
        for mand_id in range(8, 11):
            if random.random() < 0.6:  # 60% connection probability
                weight = random.uniform(2.0, 8.0)
                graph.add_edge(Edge(weak_id, mand_id, weight))
    
    # Connect weak nodes to discretionary nodes
    for weak_id in range(8):
        for disc_id in range(11, 15):
            if random.random() < 0.4:  # 40% connection probability
                weight = random.uniform(1.0, 6.0)
                graph.add_edge(Edge(weak_id, disc_id, weight))
    
    # Connect discretionary nodes to mandatory nodes
    for disc_id in range(11, 15):
        for mand_id in range(8, 11):
            if random.random() < 0.7:  # 70% connection probability
                weight = random.uniform(1.5, 5.0)
                graph.add_edge(Edge(disc_id, mand_id, weight))
    
    # Connect some discretionary nodes to each other
    for i in range(11, 14):
        for j in range(i + 1, 15):
            if random.random() < 0.3:  # 30% connection probability
                weight = random.uniform(2.0, 4.0)
                graph.add_edge(Edge(i, j, weight))
    
    return graph


def create_large_test_network() -> IoTGraph:
    """
    Create a large test network for scalability testing.
    
    Returns:
        IoTGraph: Large test network with 30 nodes
    """
    graph = IoTGraph()
    
    # Add weak nodes (sensors)
    for i in range(20):
        node = Node(i, NodeType.WEAK, capacity=1, computational_power=0.8)
        graph.add_node(node)
    
    # Add mandatory nodes (hubs)
    for i in range(20, 25):
        node = Node(i, NodeType.MANDATORY, capacity=8, computational_power=0.2)
        graph.add_node(node)
    
    # Add discretionary nodes (relays)
    for i in range(25, 30):
        node = Node(i, NodeType.DISCRETIONARY, capacity=4, computational_power=0.5)
        graph.add_node(node)
    
    # Add edges with realistic weights
    import random
    random.seed(123)
    
    # Connect weak nodes to mandatory nodes
    for weak_id in range(20):
        for mand_id in range(20, 25):
            if random.random() < 0.4:  # 40% connection probability
                weight = random.uniform(3.0, 10.0)
                graph.add_edge(Edge(weak_id, mand_id, weight))
    
    # Connect weak nodes to discretionary nodes
    for weak_id in range(20):
        for disc_id in range(25, 30):
            if random.random() < 0.3:  # 30% connection probability
                weight = random.uniform(2.0, 8.0)
                graph.add_edge(Edge(weak_id, disc_id, weight))
    
    # Connect discretionary nodes to mandatory nodes
    for disc_id in range(25, 30):
        for mand_id in range(20, 25):
            if random.random() < 0.6:  # 60% connection probability
                weight = random.uniform(2.0, 6.0)
                graph.add_edge(Edge(disc_id, mand_id, weight))
    
    # Connect some discretionary nodes to each other
    for i in range(25, 29):
        for j in range(i + 1, 30):
            if random.random() < 0.2:  # 20% connection probability
                weight = random.uniform(3.0, 5.0)
                graph.add_edge(Edge(i, j, weight))
    
    return graph


def create_disconnected_network() -> IoTGraph:
    """
    Create a disconnected network to test algorithm robustness.
    
    Returns:
        IoTGraph: Network with disconnected components
    """
    graph = IoTGraph()
    
    # Add nodes for first component
    nodes1 = [
        Node(0, NodeType.WEAK, capacity=1),
        Node(1, NodeType.MANDATORY, capacity=3),
        Node(2, NodeType.DISCRETIONARY, capacity=2)
    ]
    
    # Add nodes for second component
    nodes2 = [
        Node(3, NodeType.WEAK, capacity=1),
        Node(4, NodeType.MANDATORY, capacity=3),
        Node(5, NodeType.DISCRETIONARY, capacity=2)
    ]
    
    all_nodes = nodes1 + nodes2
    for node in all_nodes:
        graph.add_node(node)
    
    # Add edges within first component
    edges1 = [
        Edge(0, 1, 4.0),
        Edge(0, 2, 2.0),
        Edge(1, 2, 3.0)
    ]
    
    # Add edges within second component
    edges2 = [
        Edge(3, 4, 5.0),
        Edge(3, 5, 3.0),
        Edge(4, 5, 2.0)
    ]
    
    all_edges = edges1 + edges2
    for edge in all_edges:
        graph.add_edge(edge)
    
    return graph


def create_capacity_constrained_network() -> IoTGraph:
    """
    Create a network with tight capacity constraints.
    
    Returns:
        IoTGraph: Network with challenging capacity constraints
    """
    graph = IoTGraph()
    
    # Add many weak nodes
    for i in range(10):
        node = Node(i, NodeType.WEAK, capacity=1, computational_power=0.9)
        graph.add_node(node)
    
    # Add few mandatory nodes with low capacity
    for i in range(10, 12):
        node = Node(i, NodeType.MANDATORY, capacity=2, computational_power=0.2)
        graph.add_node(node)
    
    # Add some discretionary nodes
    for i in range(12, 15):
        node = Node(i, NodeType.DISCRETIONARY, capacity=2, computational_power=0.5)
        graph.add_node(node)
    
    # Add edges
    import random
    random.seed(456)
    
    # Connect weak nodes to mandatory nodes
    for weak_id in range(10):
        for mand_id in range(10, 12):
            if random.random() < 0.8:  # High connection probability
                weight = random.uniform(1.0, 5.0)
                graph.add_edge(Edge(weak_id, mand_id, weight))
    
    # Connect weak nodes to discretionary nodes
    for weak_id in range(10):
        for disc_id in range(12, 15):
            if random.random() < 0.6:  # Medium connection probability
                weight = random.uniform(1.0, 4.0)
                graph.add_edge(Edge(weak_id, disc_id, weight))
    
    # Connect discretionary nodes to mandatory nodes
    for disc_id in range(12, 15):
        for mand_id in range(10, 12):
            if random.random() < 0.7:  # High connection probability
                weight = random.uniform(1.0, 3.0)
                graph.add_edge(Edge(disc_id, mand_id, weight))
    
    return graph


def get_sample_networks() -> dict:
    """
    Get a dictionary of all sample networks.
    
    Returns:
        dict: Dictionary mapping network names to IoTGraph instances
    """
    return {
        "simple": create_simple_test_network(),
        "medium": create_medium_test_network(),
        "large": create_large_test_network(),
        "disconnected": create_disconnected_network(),
        "capacity_constrained": create_capacity_constrained_network()
    }


def print_network_summary(graph: IoTGraph, name: str = "Network"):
    """
    Print a summary of the network properties.
    
    Args:
        graph: The IoT graph to summarize
        name: Name of the network
    """
    print(f"\n{name} Summary:")
    print(f"  Total nodes: {len(graph.nodes)}")
    print(f"  Weak nodes: {len(graph.get_nodes_by_type(NodeType.WEAK))}")
    print(f"  Mandatory nodes: {len(graph.get_nodes_by_type(NodeType.MANDATORY))}")
    print(f"  Discretionary nodes: {len(graph.get_nodes_by_type(NodeType.DISCRETIONARY))}")
    print(f"  Total edges: {len(graph.edges) // 2}")
    print(f"  Connected: {graph.is_connected()}")
    
    # Calculate total capacity
    total_capacity = sum(node.capacity for node in graph.nodes.values() if node.capacity)
    print(f"  Total capacity: {total_capacity}")


if __name__ == "__main__":
    """Demo script to show sample networks."""
    print("Sample Networks Demo")
    print("=" * 50)
    
    networks = get_sample_networks()
    
    for name, graph in networks.items():
        print_network_summary(graph, name.capitalize())
    
    print("\nSample networks created successfully!")
