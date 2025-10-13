"""
Unit tests for IoT network optimization algorithms.

This module contains comprehensive tests for the MST and Steiner Tree algorithms
implemented in the chapter 16 package.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models import IoTGraph, Node, Edge, NodeType
from src.algorithms import (
    KruskalMST, PrimMST, ConstrainedMST, MSTSolution,
    GreedySteinerTree, SteinerSolution, solve_steiner_tree_constrained
)
from src.utils import GraphGenerator


class TestMSTAlgorithms(unittest.TestCase):
    """Test cases for Minimum Spanning Tree algorithms."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = self._create_test_graph()
    
    def _create_test_graph(self):
        """Create a test graph for MST algorithms."""
        graph = IoTGraph()
        
        # Add nodes
        nodes = [
            Node(0, NodeType.WEAK, capacity=1),
            Node(1, NodeType.MANDATORY, capacity=3),
            Node(2, NodeType.DISCRETIONARY, capacity=2),
            Node(3, NodeType.WEAK, capacity=1),
            Node(4, NodeType.MANDATORY, capacity=3)
        ]
        
        for node in nodes:
            graph.add_node(node)
        
        # Add edges
        edges = [
            Edge(0, 1, 5.0),
            Edge(0, 2, 3.0),
            Edge(1, 2, 2.0),
            Edge(1, 4, 4.0),
            Edge(2, 3, 1.0),
            Edge(3, 4, 6.0)
        ]
        
        for edge in edges:
            graph.add_edge(edge)
        
        return graph
    
    def test_kruskal_mst(self):
        """Test Kruskal's MST algorithm."""
        kruskal = KruskalMST(self.graph)
        solution = kruskal.solve()
        
        # Check solution properties
        self.assertIsInstance(solution, MSTSolution)
        self.assertEqual(solution.algorithm_used, "Kruskal")
        self.assertEqual(len(solution.edges), len(self.graph.nodes) - 1)
        self.assertGreater(solution.total_cost, 0)
        
        # Check that all nodes are connected
        connected_nodes = set()
        for edge in solution.edges:
            connected_nodes.add(edge[0])
            connected_nodes.add(edge[1])
        self.assertEqual(len(connected_nodes), len(self.graph.nodes))
    
    def test_prim_mst(self):
        """Test Prim's MST algorithm."""
        prim = PrimMST(self.graph)
        solution = prim.solve()
        
        # Check solution properties
        self.assertIsInstance(solution, MSTSolution)
        self.assertEqual(solution.algorithm_used, "Prim")
        self.assertEqual(len(solution.edges), len(self.graph.nodes) - 1)
        self.assertGreater(solution.total_cost, 0)
        
        # Check that all nodes are connected
        connected_nodes = set()
        for edge in solution.edges:
            connected_nodes.add(edge[0])
            connected_nodes.add(edge[1])
        self.assertEqual(len(connected_nodes), len(self.graph.nodes))
    
    def test_constrained_mst(self):
        """Test constrained MST algorithm."""
        constrained = ConstrainedMST(self.graph)
        solution = constrained.solve()
        
        # Check solution properties
        self.assertIsInstance(solution, MSTSolution)
        self.assertEqual(solution.algorithm_used, "ConstrainedPrim")
        self.assertGreater(solution.total_cost, 0)
        
        # Check capacity constraints
        node_degrees = {}
        for edge in solution.edges:
            node_degrees[edge[0]] = node_degrees.get(edge[0], 0) + 1
            node_degrees[edge[1]] = node_degrees.get(edge[1], 0) + 1
        
        for node_id, degree in node_degrees.items():
            node = self.graph.nodes[node_id]
            if node.capacity is not None:
                self.assertLessEqual(degree, node.capacity)
    
    def test_mst_algorithms_consistency(self):
        """Test that MST algorithms produce consistent results."""
        kruskal = KruskalMST(self.graph)
        prim = PrimMST(self.graph)
        
        kruskal_solution = kruskal.solve()
        prim_solution = prim.solve()
        
        # Both algorithms should produce the same total cost
        self.assertAlmostEqual(kruskal_solution.total_cost, prim_solution.total_cost, places=2)
        
        # Both should have the same number of edges
        self.assertEqual(len(kruskal_solution.edges), len(prim_solution.edges))
    
    def test_empty_graph(self):
        """Test MST algorithms with empty graph."""
        empty_graph = IoTGraph()
        
        kruskal = KruskalMST(empty_graph)
        prim = PrimMST(empty_graph)
        
        kruskal_solution = kruskal.solve()
        prim_solution = prim.solve()
        
        self.assertEqual(len(kruskal_solution.edges), 0)
        self.assertEqual(kruskal_solution.total_cost, 0.0)
        self.assertEqual(len(prim_solution.edges), 0)
        self.assertEqual(prim_solution.total_cost, 0.0)
    
    def test_single_node_graph(self):
        """Test MST algorithms with single node graph."""
        single_node_graph = IoTGraph()
        single_node_graph.add_node(Node(0, NodeType.WEAK, capacity=1))
        
        kruskal = KruskalMST(single_node_graph)
        prim = PrimMST(single_node_graph)
        
        kruskal_solution = kruskal.solve()
        prim_solution = prim.solve()
        
        self.assertEqual(len(kruskal_solution.edges), 0)
        self.assertEqual(kruskal_solution.total_cost, 0.0)
        self.assertEqual(len(prim_solution.edges), 0)
        self.assertEqual(prim_solution.total_cost, 0.0)


class TestSteinerTreeAlgorithms(unittest.TestCase):
    """Test cases for Steiner Tree algorithms."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = self._create_test_graph()
    
    def _create_test_graph(self):
        """Create a test graph for Steiner Tree algorithms."""
        graph = IoTGraph()
        
        # Add nodes
        nodes = [
            Node(0, NodeType.WEAK, capacity=1),      # Weak node 1
            Node(1, NodeType.WEAK, capacity=1),      # Weak node 2
            Node(2, NodeType.MANDATORY, capacity=3), # Mandatory node 1
            Node(3, NodeType.MANDATORY, capacity=3), # Mandatory node 2
            Node(4, NodeType.DISCRETIONARY, capacity=2), # Discretionary node 1
            Node(5, NodeType.DISCRETIONARY, capacity=2)  # Discretionary node 2
        ]
        
        for node in nodes:
            graph.add_node(node)
        
        # Add edges
        edges = [
            Edge(0, 2, 5.0),  # Weak to mandatory
            Edge(0, 4, 3.0),  # Weak to discretionary
            Edge(1, 3, 4.0),  # Weak to mandatory
            Edge(1, 5, 2.0),  # Weak to discretionary
            Edge(2, 3, 6.0),  # Mandatory to mandatory
            Edge(2, 4, 2.0),  # Mandatory to discretionary
            Edge(3, 5, 3.0),  # Mandatory to discretionary
            Edge(4, 5, 1.0)   # Discretionary to discretionary
        ]
        
        for edge in edges:
            graph.add_edge(edge)
        
        return graph
    
    def test_greedy_steiner_tree(self):
        """Test greedy Steiner Tree algorithm."""
        steiner = GreedySteinerTree(self.graph)
        solution = steiner.solve()
        
        # Check solution properties
        self.assertIsInstance(solution, SteinerSolution)
        self.assertGreaterEqual(len(solution.connected_nodes), 0)
        self.assertGreaterEqual(solution.total_cost, 0)
        self.assertIsInstance(solution.capacity_violations, int)
        self.assertIsInstance(solution.unconnected_weak_nodes, list)
        self.assertIsInstance(solution.used_discretionary_nodes, set)
        
        # Check that all mandatory nodes are connected
        mandatory_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        for node in mandatory_nodes:
            self.assertIn(node.id, solution.connected_nodes)
    
    def test_steiner_tree_without_discretionary(self):
        """Test Steiner Tree without discretionary nodes."""
        steiner = GreedySteinerTree(self.graph)
        solution = steiner.solve([])
        
        # Check that no discretionary nodes are used
        discretionary_nodes = self.graph.get_nodes_by_type(NodeType.DISCRETIONARY)
        for node in discretionary_nodes:
            self.assertNotIn(node.id, solution.used_discretionary_nodes)
    
    def test_steiner_tree_with_all_discretionary(self):
        """Test Steiner Tree with all discretionary nodes."""
        steiner = GreedySteinerTree(self.graph)
        all_discretionary = [n.id for n in self.graph.get_nodes_by_type(NodeType.DISCRETIONARY)]
        solution = steiner.solve(all_discretionary)
        
        # Check that some discretionary nodes might be used
        self.assertGreaterEqual(len(solution.used_discretionary_nodes), 0)
    
    def test_solve_steiner_tree_constrained(self):
        """Test the main Steiner Tree solving function."""
        solution = solve_steiner_tree_constrained(self.graph)
        
        # Check solution properties
        self.assertIsInstance(solution, SteinerSolution)
        self.assertGreaterEqual(len(solution.connected_nodes), 0)
        self.assertGreaterEqual(solution.total_cost, 0)
        
        # Check that all mandatory nodes are connected
        mandatory_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        for node in mandatory_nodes:
            self.assertIn(node.id, solution.connected_nodes)
    
    def test_steiner_tree_objective_function(self):
        """Test Steiner Tree objective function calculation."""
        steiner = GreedySteinerTree(self.graph)
        solution = steiner.solve()
        
        # Test objective function with different alpha values
        score_alpha_0 = solution.get_score(alpha=0.0)
        score_alpha_1 = solution.get_score(alpha=1.0)
        score_alpha_05 = solution.get_score(alpha=0.5)
        
        self.assertGreaterEqual(score_alpha_0, 0)
        self.assertGreaterEqual(score_alpha_1, 0)
        self.assertGreaterEqual(score_alpha_05, 0)
        
        # Score should be between the two extreme values
        self.assertLessEqual(score_alpha_05, max(score_alpha_0, score_alpha_1))
        self.assertGreaterEqual(score_alpha_05, min(score_alpha_0, score_alpha_1))
    
    def test_empty_graph_steiner(self):
        """Test Steiner Tree with empty graph."""
        empty_graph = IoTGraph()
        steiner = GreedySteinerTree(empty_graph)
        solution = steiner.solve()
        
        self.assertEqual(len(solution.connected_nodes), 0)
        self.assertEqual(solution.total_cost, 0.0)
        self.assertEqual(solution.capacity_violations, 0)
        self.assertEqual(len(solution.unconnected_weak_nodes), 0)
        self.assertEqual(len(solution.used_discretionary_nodes), 0)
    
    def test_single_node_steiner(self):
        """Test Steiner Tree with single node."""
        single_node_graph = IoTGraph()
        single_node_graph.add_node(Node(0, NodeType.MANDATORY, capacity=3))
        
        steiner = GreedySteinerTree(single_node_graph)
        solution = steiner.solve()
        
        self.assertIn(0, solution.connected_nodes)
        self.assertEqual(solution.total_cost, 0.0)
        self.assertEqual(solution.capacity_violations, 0)


class TestGraphGenerator(unittest.TestCase):
    """Test cases for graph generation utilities."""
    
    def test_random_iot_network(self):
        """Test random IoT network generation."""
        generator = GraphGenerator(seed=42)
        graph = generator.generate_random_iot_network(
            num_weak=5,
            num_mandatory=3,
            num_discretionary=2
        )
        
        # Check node counts
        self.assertEqual(len(graph.get_nodes_by_type(NodeType.WEAK)), 5)
        self.assertEqual(len(graph.get_nodes_by_type(NodeType.MANDATORY)), 3)
        self.assertEqual(len(graph.get_nodes_by_type(NodeType.DISCRETIONARY)), 2)
        
        # Check that all nodes have capacity
        for node in graph.nodes.values():
            self.assertIsNotNone(node.capacity)
            self.assertGreater(node.capacity, 0)
    
    def test_grid_iot_network(self):
        """Test grid IoT network generation."""
        generator = GraphGenerator(seed=42)
        graph = generator.generate_grid_iot_network(grid_size=4)
        
        # Check that all nodes have positions
        for node in graph.nodes.values():
            self.assertIsNotNone(node.position)
            self.assertEqual(len(node.position), 2)
    
    def test_fire_detection_network(self):
        """Test fire detection network generation."""
        generator = GraphGenerator(seed=42)
        graph = generator.generate_fire_detection_network()
        
        # Check node types
        weak_nodes = graph.get_nodes_by_type(NodeType.WEAK)
        mandatory_nodes = graph.get_nodes_by_type(NodeType.MANDATORY)
        discretionary_nodes = graph.get_nodes_by_type(NodeType.DISCRETIONARY)
        
        self.assertGreater(len(weak_nodes), 0)
        self.assertGreater(len(mandatory_nodes), 0)
        self.assertGreater(len(discretionary_nodes), 0)
        
        # Check that all nodes have positions
        for node in graph.nodes.values():
            self.assertIsNotNone(node.position)
    
    def test_drone_network(self):
        """Test drone network generation."""
        generator = GraphGenerator(seed=42)
        graph = generator.generate_drone_network()
        
        # Check node types
        weak_nodes = graph.get_nodes_by_type(NodeType.WEAK)
        mandatory_nodes = graph.get_nodes_by_type(NodeType.MANDATORY)
        discretionary_nodes = graph.get_nodes_by_type(NodeType.DISCRETIONARY)
        
        self.assertGreater(len(weak_nodes), 0)
        self.assertGreater(len(mandatory_nodes), 0)
        self.assertGreater(len(discretionary_nodes), 0)
        
        # Check that all nodes have positions
        for node in graph.nodes.values():
            self.assertIsNotNone(node.position)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # Generate a test network
        generator = GraphGenerator(seed=42)
        graph = generator.generate_random_iot_network(
            num_weak=8,
            num_mandatory=3,
            num_discretionary=2
        )
        
        # Test MST algorithms
        from src.algorithms import compare_mst_algorithms
        mst_results = compare_mst_algorithms(graph)
        
        self.assertGreater(len(mst_results), 0)
        for name, solution in mst_results.items():
            self.assertIsInstance(solution, MSTSolution)
            self.assertGreater(solution.total_cost, 0)
        
        # Test Steiner Tree algorithm
        steiner_solution = solve_steiner_tree_constrained(graph)
        self.assertIsInstance(steiner_solution, SteinerSolution)
        self.assertGreaterEqual(steiner_solution.total_cost, 0)
        
        # Test that mandatory nodes are connected
        mandatory_nodes = graph.get_nodes_by_type(NodeType.MANDATORY)
        for node in mandatory_nodes:
            self.assertIn(node.id, steiner_solution.connected_nodes)
    
    def test_algorithm_consistency(self):
        """Test algorithm consistency across different network sizes."""
        generator = GraphGenerator(seed=42)
        
        for size in [5, 10, 15]:
            graph = generator.generate_random_iot_network(
                num_weak=size,
                num_mandatory=3,
                num_discretionary=2
            )
            
            # Test MST algorithms
            from src.algorithms import compare_mst_algorithms
            mst_results = compare_mst_algorithms(graph)
            
            # All MST algorithms should produce valid solutions
            for name, solution in mst_results.items():
                self.assertIsInstance(solution, MSTSolution)
                self.assertGreater(solution.total_cost, 0)
                self.assertEqual(len(solution.edges), len(graph.nodes) - 1)
            
            # Test Steiner Tree algorithm
            steiner_solution = solve_steiner_tree_constrained(graph)
            self.assertIsInstance(steiner_solution, SteinerSolution)
            self.assertGreaterEqual(steiner_solution.total_cost, 0)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
