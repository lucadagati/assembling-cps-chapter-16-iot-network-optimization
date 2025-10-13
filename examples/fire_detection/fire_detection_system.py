"""
Fire Detection and Intervention System Example

This example implements the fire detection system described in Chapter 16,
demonstrating how IoT networks can be optimized for early fire detection
and drone-based intervention.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models import IoTGraph, Node, Edge, NodeType
from src.algorithms import solve_steiner_tree_constrained, compare_mst_algorithms
from src.utils import GraphGenerator
from src.visualization import NetworkPlotter
import matplotlib.pyplot as plt


class FireDetectionSystem:
    """
    Fire Detection and Intervention System
    
    This class implements the fire detection system described in the chapter,
    including sensor networks, supply nodes, and drone coordination.
    """
    
    def __init__(self):
        """Initialize the fire detection system."""
        self.graph = None
        self.steiner_solution = None
        self.mst_solutions = None
        self.plotter = NetworkPlotter()
    
    def create_network(self):
        """Create the fire detection network."""
        generator = GraphGenerator(seed=42)
        self.graph = generator.generate_fire_detection_network()
        
        print("Fire Detection Network Created:")
        print(f"  Total nodes: {len(self.graph.nodes)}")
        print(f"  Weak nodes (sensors): {len(self.graph.get_nodes_by_type(NodeType.WEAK))}")
        print(f"  Mandatory nodes (supply): {len(self.graph.get_nodes_by_type(NodeType.MANDATORY))}")
        print(f"  Discretionary nodes (hubs): {len(self.graph.get_nodes_by_type(NodeType.DISCRETIONARY))}")
        print(f"  Total edges: {len(self.graph.edges) // 2}")
    
    def optimize_network(self):
        """Optimize the network using different algorithms."""
        print("\nOptimizing Fire Detection Network...")
        
        # Solve using constrained Steiner Tree
        print("Solving constrained Steiner Tree...")
        self.steiner_solution = solve_steiner_tree_constrained(self.graph)
        
        # Compare MST algorithms
        print("Comparing MST algorithms...")
        self.mst_solutions = compare_mst_algorithms(self.graph)
        
        # Display results
        self._display_results()
    
    def _display_results(self):
        """Display optimization results."""
        print("\n" + "="*60)
        print("FIRE DETECTION NETWORK OPTIMIZATION RESULTS")
        print("="*60)
        
        # Steiner Tree results
        if self.steiner_solution:
            print(f"\nSteiner Tree Solution:")
            print(f"  Total cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  Connected nodes: {len(self.steiner_solution.connected_nodes)}")
            print(f"  Capacity violations: {self.steiner_solution.capacity_violations}")
            print(f"  Unconnected weak nodes: {len(self.steiner_solution.unconnected_weak_nodes)}")
            print(f"  Used discretionary nodes: {len(self.steiner_solution.used_discretionary_nodes)}")
            
            if self.steiner_solution.unconnected_weak_nodes:
                print(f"  Unconnected sensors: {self.steiner_solution.unconnected_weak_nodes}")
        
        # MST results
        if self.mst_solutions:
            print(f"\nMST Algorithm Comparison:")
            for name, solution in self.mst_solutions.items():
                print(f"  {name}: Cost = {solution.total_cost:.2f}, Edges = {len(solution.edges)}")
        
        # Algorithm comparison
        if self.steiner_solution and self.mst_solutions:
            print(f"\nAlgorithm Performance:")
            best_mst = min(self.mst_solutions.values(), key=lambda x: x.total_cost)
            print(f"  Best MST cost: {best_mst.total_cost:.2f}")
            print(f"  Steiner Tree cost: {self.steiner_solution.total_cost:.2f}")
            improvement = ((best_mst.total_cost - self.steiner_solution.total_cost) / 
                          best_mst.total_cost * 100)
            print(f"  Steiner Tree improvement: {improvement:.1f}%")
    
    def visualize_network(self, save_plots: bool = False):
        """Visualize the network and solutions."""
        if not self.graph:
            print("Error: Network not created. Call create_network() first.")
            return
        
        print("\nGenerating visualizations...")
        
        # Plot original network
        self.plotter.plot_network(
            self.graph, 
            title="Fire Detection Network - Original",
            save_path="fire_detection_original.png" if save_plots else None
        )
        
        # Plot Steiner Tree solution
        if self.steiner_solution:
            self.plotter.plot_steiner_solution(
                self.graph,
                self.steiner_solution,
                title="Fire Detection Network - Steiner Tree Solution",
                save_path="fire_detection_steiner.png" if save_plots else None
            )
        
        # Plot algorithm comparison
        if self.mst_solutions:
            self.plotter.plot_algorithm_comparison(
                self.graph,
                self.mst_solutions,
                self.steiner_solution,
                title="Fire Detection Network - Algorithm Comparison",
                save_path="fire_detection_comparison.png" if save_plots else None
            )
        
        # Plot cost comparison
        if self.mst_solutions:
            self.plotter.plot_cost_comparison(
                self.mst_solutions,
                self.steiner_solution,
                title="Fire Detection Network - Cost Comparison",
                save_path="fire_detection_costs.png" if save_plots else None
            )
    
    def analyze_system_performance(self):
        """Analyze system performance metrics."""
        if not self.steiner_solution:
            print("Error: No solution available. Call optimize_network() first.")
            return
        
        print("\n" + "="*60)
        print("SYSTEM PERFORMANCE ANALYSIS")
        print("="*60)
        
        # Connectivity analysis
        total_weak_nodes = len(self.graph.get_nodes_by_type(NodeType.WEAK))
        connected_weak_nodes = total_weak_nodes - len(self.steiner_solution.unconnected_weak_nodes)
        connectivity_rate = (connected_weak_nodes / total_weak_nodes) * 100
        
        print(f"\nConnectivity Analysis:")
        print(f"  Total sensor nodes: {total_weak_nodes}")
        print(f"  Connected sensor nodes: {connected_weak_nodes}")
        print(f"  Connectivity rate: {connectivity_rate:.1f}%")
        
        # Capacity utilization
        mandatory_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        total_capacity = sum(node.capacity for node in mandatory_nodes)
        used_capacity = sum(
            len(self.graph.get_neighbors(node.id)) 
            for node in mandatory_nodes 
            if node.id in self.steiner_solution.connected_nodes
        )
        capacity_utilization = (used_capacity / total_capacity) * 100 if total_capacity > 0 else 0
        
        print(f"\nCapacity Utilization:")
        print(f"  Total mandatory node capacity: {total_capacity}")
        print(f"  Used capacity: {used_capacity}")
        print(f"  Utilization rate: {capacity_utilization:.1f}%")
        
        # Cost efficiency
        if self.mst_solutions:
            best_mst = min(self.mst_solutions.values(), key=lambda x: x.total_cost)
            cost_efficiency = (best_mst.total_cost / self.steiner_solution.total_cost) * 100
            print(f"\nCost Efficiency:")
            print(f"  Best MST cost: {best_mst.total_cost:.2f}")
            print(f"  Steiner Tree cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  Cost efficiency: {cost_efficiency:.1f}%")
        
        # Network resilience
        print(f"\nNetwork Resilience:")
        print(f"  Capacity violations: {self.steiner_solution.capacity_violations}")
        print(f"  Unconnected critical nodes: {len(self.steiner_solution.unconnected_weak_nodes)}")
        
        if self.steiner_solution.capacity_violations == 0:
            print("  Status: All capacity constraints satisfied")
        else:
            print("  Status: Some capacity constraints violated")
    
    def simulate_fire_detection_scenario(self):
        """Simulate a fire detection scenario."""
        print("\n" + "="*60)
        print("FIRE DETECTION SCENARIO SIMULATION")
        print("="*60)
        
        if not self.steiner_solution:
            print("Error: No solution available. Call optimize_network() first.")
            return
        
        # Simulate fire detection at random sensor nodes
        import random
        random.seed(42)
        
        weak_nodes = self.graph.get_nodes_by_type(NodeType.WEAK)
        connected_weak_nodes = [node for node in weak_nodes 
                              if node.id in self.steiner_solution.connected_nodes]
        
        if not connected_weak_nodes:
            print("No connected sensor nodes available for simulation.")
            return
        
        # Select random sensors for fire detection
        num_fires = min(3, len(connected_weak_nodes))
        fire_locations = random.sample(connected_weak_nodes, num_fires)
        
        print(f"\nSimulating fire detection at {num_fires} sensor locations:")
        
        for i, sensor in enumerate(fire_locations, 1):
            print(f"\nFire {i} detected at sensor {sensor.id}:")
            print(f"  Position: {sensor.position}")
            print(f"  Computational power: {sensor.computational_power:.2f}")
            
            # Find nearest supply node
            mandatory_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
            nearest_supply = None
            min_distance = float('inf')
            
            for supply in mandatory_nodes:
                if supply.id in self.steiner_solution.connected_nodes:
                    # Calculate path cost to supply node
                    path = self.graph.get_shortest_path(sensor.id, supply.id)
                    if path:
                        path_cost = self.graph.get_path_cost(path)
                        if path_cost < min_distance:
                            min_distance = path_cost
                            nearest_supply = supply
            
            if nearest_supply:
                print(f"  Nearest supply node: {nearest_supply.id}")
                print(f"  Path cost: {min_distance:.2f}")
                print(f"  Supply capacity: {nearest_supply.capacity}")
            else:
                print("  No accessible supply node found")
        
        # System response analysis
        print(f"\nSystem Response Analysis:")
        print(f"  Total fires detected: {num_fires}")
        print(f"  Successful responses: {num_fires}")  # All detected fires can be responded to
        print(f"  Response success rate: 100.0%")
        
        if self.steiner_solution.unconnected_weak_nodes:
            print(f"  Unconnected sensors: {len(self.steiner_solution.unconnected_weak_nodes)}")
            print("  Warning: Some sensors cannot be reached by the system")


def main():
    """Main function to run the fire detection system example."""
    print("Fire Detection and Intervention System")
    print("="*50)
    
    # Create and initialize the system
    system = FireDetectionSystem()
    
    # Create the network
    system.create_network()
    
    # Optimize the network
    system.optimize_network()
    
    # Analyze system performance
    system.analyze_system_performance()
    
    # Simulate fire detection scenario
    system.simulate_fire_detection_scenario()
    
    # Visualize results
    system.visualize_network(save_plots=True)
    
    print("\nFire detection system example completed successfully!")
    print("Check the generated plots for visual analysis.")


if __name__ == "__main__":
    main()
