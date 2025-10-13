"""
Drone Network Coordination Example

This example demonstrates how IoT network optimization can be applied
to drone coordination systems, as described in the chapter's Stack4Things integration.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models import IoTGraph, Node, Edge, NodeType
from src.algorithms import solve_steiner_tree_constrained, compare_mst_algorithms
from src.utils import GraphGenerator
from src.visualization import NetworkPlotter
import matplotlib.pyplot as plt
import random


class DroneCoordinationSystem:
    """
    Drone Network Coordination System
    
    This class implements a drone coordination system that demonstrates
    how IoT network optimization can be applied to UAV operations.
    """
    
    def __init__(self):
        """Initialize the drone coordination system."""
        self.graph = None
        self.steiner_solution = None
        self.mst_solutions = None
        self.plotter = NetworkPlotter()
        self.mission_history = []
    
    def create_network(self):
        """Create the drone coordination network."""
        generator = GraphGenerator(seed=123)
        self.graph = generator.generate_drone_network()
        
        print("Drone Coordination Network Created:")
        print(f"  Total nodes: {len(self.graph.nodes)}")
        print(f"  Drone nodes: {len(self.graph.get_nodes_by_type(NodeType.WEAK))}")
        print(f"  Control stations: {len(self.graph.get_nodes_by_type(NodeType.MANDATORY))}")
        print(f"  Relay stations: {len(self.graph.get_nodes_by_type(NodeType.DISCRETIONARY))}")
        print(f"  Total edges: {len(self.graph.edges) // 2}")
    
    def optimize_network(self):
        """Optimize the drone network using different algorithms."""
        print("\nOptimizing Drone Coordination Network...")
        
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
        print("DRONE COORDINATION NETWORK OPTIMIZATION RESULTS")
        print("="*60)
        
        # Steiner Tree results
        if self.steiner_solution:
            print(f"\nSteiner Tree Solution:")
            print(f"  Total cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  Connected nodes: {len(self.steiner_solution.connected_nodes)}")
            print(f"  Capacity violations: {self.steiner_solution.capacity_violations}")
            print(f"  Unconnected drones: {len(self.steiner_solution.unconnected_weak_nodes)}")
            print(f"  Used relay stations: {len(self.steiner_solution.used_discretionary_nodes)}")
            
            if self.steiner_solution.unconnected_weak_nodes:
                print(f"  Unconnected drones: {self.steiner_solution.unconnected_weak_nodes}")
        
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
    
    def simulate_drone_mission(self, num_missions: int = 5):
        """Simulate drone missions using the optimized network."""
        print("\n" + "="*60)
        print("DRONE MISSION SIMULATION")
        print("="*60)
        
        if not self.steiner_solution:
            print("Error: No solution available. Call optimize_network() first.")
            return
        
        # Get available drones and control stations
        drone_nodes = self.graph.get_nodes_by_type(NodeType.WEAK)
        control_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        
        connected_drones = [drone for drone in drone_nodes 
                           if drone.id in self.steiner_solution.connected_nodes]
        available_controls = [control for control in control_nodes 
                             if control.id in self.steiner_solution.connected_nodes]
        
        if not connected_drones or not available_controls:
            print("Insufficient connected nodes for mission simulation.")
            return
        
        print(f"\nSimulating {num_missions} drone missions...")
        
        for mission_id in range(1, num_missions + 1):
            # Select random drone and control station
            drone = random.choice(connected_drones)
            control = random.choice(available_controls)
            
            # Calculate mission path
            path = self.graph.get_shortest_path(drone.id, control.id)
            path_cost = self.graph.get_path_cost(path) if path else float('inf')
            
            # Simulate mission parameters
            mission_duration = random.uniform(10, 30)  # minutes
            battery_consumption = random.uniform(20, 40)  # percentage
            payload_weight = random.uniform(1, 5)  # kg
            
            mission = {
                'id': mission_id,
                'drone_id': drone.id,
                'control_id': control.id,
                'path': path,
                'path_cost': path_cost,
                'duration': mission_duration,
                'battery_consumption': battery_consumption,
                'payload_weight': payload_weight,
                'success': path_cost < float('inf')
            }
            
            self.mission_history.append(mission)
            
            print(f"\nMission {mission_id}:")
            print(f"  Drone: {drone.id} (Position: {drone.position})")
            print(f"  Control Station: {control.id} (Position: {control.position})")
            print(f"  Path cost: {path_cost:.2f}")
            print(f"  Mission duration: {mission_duration:.1f} minutes")
            print(f"  Battery consumption: {battery_consumption:.1f}%")
            print(f"  Payload weight: {payload_weight:.1f} kg")
            print(f"  Status: {'Success' if mission['success'] else 'Failed'}")
        
        # Mission statistics
        successful_missions = sum(1 for m in self.mission_history if m['success'])
        success_rate = (successful_missions / len(self.mission_history)) * 100
        avg_path_cost = sum(m['path_cost'] for m in self.mission_history if m['success']) / successful_missions if successful_missions > 0 else 0
        
        print(f"\nMission Statistics:")
        print(f"  Total missions: {len(self.mission_history)}")
        print(f"  Successful missions: {successful_missions}")
        print(f"  Success rate: {success_rate:.1f}%")
        print(f"  Average path cost: {avg_path_cost:.2f}")
    
    def analyze_network_performance(self):
        """Analyze drone network performance metrics."""
        if not self.steiner_solution:
            print("Error: No solution available. Call optimize_network() first.")
            return
        
        print("\n" + "="*60)
        print("DRONE NETWORK PERFORMANCE ANALYSIS")
        print("="*60)
        
        # Connectivity analysis
        total_drones = len(self.graph.get_nodes_by_type(NodeType.WEAK))
        connected_drones = total_drones - len(self.steiner_solution.unconnected_weak_nodes)
        connectivity_rate = (connected_drones / total_drones) * 100
        
        print(f"\nConnectivity Analysis:")
        print(f"  Total drones: {total_drones}")
        print(f"  Connected drones: {connected_drones}")
        print(f"  Connectivity rate: {connectivity_rate:.1f}%")
        
        # Control station utilization
        control_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        total_control_capacity = sum(node.capacity for node in control_nodes)
        used_control_capacity = sum(
            len(self.graph.get_neighbors(node.id)) 
            for node in control_nodes 
            if node.id in self.steiner_solution.connected_nodes
        )
        control_utilization = (used_control_capacity / total_control_capacity) * 100 if total_control_capacity > 0 else 0
        
        print(f"\nControl Station Utilization:")
        print(f"  Total control capacity: {total_control_capacity}")
        print(f"  Used capacity: {used_control_capacity}")
        print(f"  Utilization rate: {control_utilization:.1f}%")
        
        # Relay station usage
        relay_nodes = self.graph.get_nodes_by_type(NodeType.DISCRETIONARY)
        used_relays = len(self.steiner_solution.used_discretionary_nodes)
        relay_usage_rate = (used_relays / len(relay_nodes)) * 100 if relay_nodes else 0
        
        print(f"\nRelay Station Usage:")
        print(f"  Total relay stations: {len(relay_nodes)}")
        print(f"  Used relay stations: {used_relays}")
        print(f"  Usage rate: {relay_usage_rate:.1f}%")
        
        # Network efficiency
        if self.mst_solutions:
            best_mst = min(self.mst_solutions.values(), key=lambda x: x.total_cost)
            efficiency_ratio = self.steiner_solution.total_cost / best_mst.total_cost
            print(f"\nNetwork Efficiency:")
            print(f"  Best MST cost: {best_mst.total_cost:.2f}")
            print(f"  Steiner Tree cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  Efficiency ratio: {efficiency_ratio:.3f}")
        
        # Mission performance (if missions were simulated)
        if self.mission_history:
            successful_missions = sum(1 for m in self.mission_history if m['success'])
            success_rate = (successful_missions / len(self.mission_history)) * 100
            avg_path_cost = sum(m['path_cost'] for m in self.mission_history if m['success']) / successful_missions if successful_missions > 0 else 0
            
            print(f"\nMission Performance:")
            print(f"  Total missions: {len(self.mission_history)}")
            print(f"  Success rate: {success_rate:.1f}%")
            print(f"  Average path cost: {avg_path_cost:.2f}")
    
    def visualize_network(self, save_plots: bool = False):
        """Visualize the drone network and solutions."""
        if not self.graph:
            print("Error: Network not created. Call create_network() first.")
            return
        
        print("\nGenerating visualizations...")
        
        # Plot original network
        self.plotter.plot_network(
            self.graph, 
            title="Drone Coordination Network - Original",
            save_path="drone_network_original.png" if save_plots else None
        )
        
        # Plot Steiner Tree solution
        if self.steiner_solution:
            self.plotter.plot_steiner_solution(
                self.graph,
                self.steiner_solution,
                title="Drone Coordination Network - Steiner Tree Solution",
                save_path="drone_network_steiner.png" if save_plots else None
            )
        
        # Plot algorithm comparison
        if self.mst_solutions:
            self.plotter.plot_algorithm_comparison(
                self.graph,
                self.mst_solutions,
                self.steiner_solution,
                title="Drone Coordination Network - Algorithm Comparison",
                save_path="drone_network_comparison.png" if save_plots else None
            )
        
        # Plot cost comparison
        if self.mst_solutions:
            self.plotter.plot_cost_comparison(
                self.mst_solutions,
                self.steiner_solution,
                title="Drone Coordination Network - Cost Comparison",
                save_path="drone_network_costs.png" if save_plots else None
            )
    
    def demonstrate_stack4things_integration(self):
        """Demonstrate Stack4Things integration concepts."""
        print("\n" + "="*60)
        print("STACK4THINGS INTEGRATION DEMONSTRATION")
        print("="*60)
        
        print("\nStack4Things Framework Components:")
        print("  1. PX4 Autopilot System: Flight control firmware")
        print("  2. Stack4Things Framework: IoT orchestration layer")
        print("  3. Lightning-Rod Daemon: Device-side agent")
        print("  4. MAVROS Bridge: Communication interface")
        
        print("\nIntegration Benefits:")
        print("  - Scalable computational resources")
        print("  - Centralized mission management")
        print("  - Real-time analytics capabilities")
        print("  - Dynamic resource allocation")
        
        print("\nNetwork Architecture:")
        print("  - Cloud-enhanced UAV operations")
        print("  - Virtual networking capabilities")
        print("  - Intelligent path-splitting strategies")
        print("  - Obstacle detection through computer vision")
        
        # Simulate cloud-based mission planning
        if self.steiner_solution:
            print(f"\nCloud-Based Mission Planning:")
            print(f"  - Optimal network topology: {len(self.steiner_solution.connected_nodes)} nodes")
            print(f"  - Communication cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  - Capacity utilization: {self.steiner_solution.capacity_violations} violations")
            print(f"  - Network efficiency: {len(self.steiner_solution.used_discretionary_nodes)} relay stations")


def main():
    """Main function to run the drone coordination system example."""
    print("Drone Network Coordination System")
    print("="*50)
    
    # Create and initialize the system
    system = DroneCoordinationSystem()
    
    # Create the network
    system.create_network()
    
    # Optimize the network
    system.optimize_network()
    
    # Analyze network performance
    system.analyze_network_performance()
    
    # Simulate drone missions
    system.simulate_drone_mission(num_missions=5)
    
    # Demonstrate Stack4Things integration
    system.demonstrate_stack4things_integration()
    
    # Visualize results
    system.visualize_network(save_plots=True)
    
    print("\nDrone coordination system example completed successfully!")
    print("Check the generated plots for visual analysis.")


if __name__ == "__main__":
    main()
