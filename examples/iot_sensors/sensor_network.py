"""
IoT Sensor Network Example

This example demonstrates how IoT network optimization can be applied
to sensor networks for environmental monitoring and data collection.
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
import numpy as np


class SensorNetworkSystem:
    """
    IoT Sensor Network System
    
    This class implements a sensor network system that demonstrates
    how IoT network optimization can be applied to environmental monitoring.
    """
    
    def __init__(self):
        """Initialize the sensor network system."""
        self.graph = None
        self.steiner_solution = None
        self.mst_solutions = None
        self.plotter = NetworkPlotter()
        self.sensor_data = {}
        self.data_collection_history = []
    
    def create_network(self):
        """Create the sensor network."""
        generator = GraphGenerator(seed=456)
        self.graph = generator.generate_random_iot_network(
            num_weak=12,      # Sensor nodes
            num_mandatory=3,  # Data collection hubs
            num_discretionary=2,  # Relay nodes
            connection_probability=0.4,
            weight_range=(1.0, 15.0),
            capacity_range=(3, 8)
        )
        
        print("IoT Sensor Network Created:")
        print(f"  Total nodes: {len(self.graph.nodes)}")
        print(f"  Sensor nodes: {len(self.graph.get_nodes_by_type(NodeType.WEAK))}")
        print(f"  Data hubs: {len(self.graph.get_nodes_by_type(NodeType.MANDATORY))}")
        print(f"  Relay nodes: {len(self.graph.get_nodes_by_type(NodeType.DISCRETIONARY))}")
        print(f"  Total edges: {len(self.graph.edges) // 2}")
    
    def optimize_network(self):
        """Optimize the sensor network using different algorithms."""
        print("\nOptimizing IoT Sensor Network...")
        
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
        print("IoT SENSOR NETWORK OPTIMIZATION RESULTS")
        print("="*60)
        
        # Steiner Tree results
        if self.steiner_solution:
            print(f"\nSteiner Tree Solution:")
            print(f"  Total cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  Connected nodes: {len(self.steiner_solution.connected_nodes)}")
            print(f"  Capacity violations: {self.steiner_solution.capacity_violations}")
            print(f"  Unconnected sensors: {len(self.steiner_solution.unconnected_weak_nodes)}")
            print(f"  Used relay nodes: {len(self.steiner_solution.used_discretionary_nodes)}")
            
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
    
    def simulate_data_collection(self, num_rounds: int = 10):
        """Simulate data collection from sensors."""
        print("\n" + "="*60)
        print("SENSOR DATA COLLECTION SIMULATION")
        print("="*60)
        
        if not self.steiner_solution:
            print("Error: No solution available. Call optimize_network() first.")
            return
        
        # Get connected sensors
        sensor_nodes = self.graph.get_nodes_by_type(NodeType.WEAK)
        connected_sensors = [sensor for sensor in sensor_nodes 
                           if sensor.id in self.steiner_solution.connected_nodes]
        
        if not connected_sensors:
            print("No connected sensors available for data collection.")
            return
        
        print(f"\nSimulating data collection for {num_rounds} rounds...")
        
        for round_id in range(1, num_rounds + 1):
            print(f"\nData Collection Round {round_id}:")
            
            # Simulate data collection from each connected sensor
            total_data_collected = 0
            successful_transmissions = 0
            
            for sensor in connected_sensors:
                # Simulate sensor data generation
                data_size = random.uniform(1, 10)  # KB
                battery_level = random.uniform(20, 100)  # percentage
                signal_strength = random.uniform(0.5, 1.0)  # normalized
                
                # Check if sensor can transmit data
                can_transmit = (battery_level > 30 and signal_strength > 0.6)
                
                if can_transmit:
                    # Find path to nearest data hub
                    hub_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
                    nearest_hub = None
                    min_cost = float('inf')
                    
                    for hub in hub_nodes:
                        if hub.id in self.steiner_solution.connected_nodes:
                            path = self.graph.get_shortest_path(sensor.id, hub.id)
                            if path:
                                path_cost = self.graph.get_path_cost(path)
                                if path_cost < min_cost:
                                    min_cost = path_cost
                                    nearest_hub = hub
                    
                    if nearest_hub:
                        # Simulate data transmission
                        transmission_success = random.uniform(0.8, 1.0) > 0.1  # 90% success rate
                        
                        if transmission_success:
                            total_data_collected += data_size
                            successful_transmissions += 1
                            
                            # Store sensor data
                            if sensor.id not in self.sensor_data:
                                self.sensor_data[sensor.id] = []
                            
                            self.sensor_data[sensor.id].append({
                                'round': round_id,
                                'data_size': data_size,
                                'battery_level': battery_level,
                                'signal_strength': signal_strength,
                                'transmission_cost': min_cost,
                                'hub_id': nearest_hub.id
                            })
                
                print(f"  Sensor {sensor.id}: Data={data_size:.1f}KB, "
                      f"Battery={battery_level:.1f}%, "
                      f"Signal={signal_strength:.2f}, "
                      f"Status={'Success' if can_transmit else 'Failed'}")
            
            # Round statistics
            transmission_rate = (successful_transmissions / len(connected_sensors)) * 100
            print(f"  Round {round_id} Summary:")
            print(f"    Total data collected: {total_data_collected:.1f} KB")
            print(f"    Successful transmissions: {successful_transmissions}/{len(connected_sensors)}")
            print(f"    Transmission rate: {transmission_rate:.1f}%")
            
            # Store round data
            self.data_collection_history.append({
                'round': round_id,
                'total_data': total_data_collected,
                'successful_transmissions': successful_transmissions,
                'transmission_rate': transmission_rate
            })
        
        # Overall statistics
        total_data = sum(round_data['total_data'] for round_data in self.data_collection_history)
        avg_transmission_rate = np.mean([round_data['transmission_rate'] 
                                       for round_data in self.data_collection_history])
        
        print(f"\nData Collection Summary:")
        print(f"  Total rounds: {num_rounds}")
        print(f"  Total data collected: {total_data:.1f} KB")
        print(f"  Average transmission rate: {avg_transmission_rate:.1f}%")
        print(f"  Connected sensors: {len(connected_sensors)}")
    
    def analyze_network_performance(self):
        """Analyze sensor network performance metrics."""
        if not self.steiner_solution:
            print("Error: No solution available. Call optimize_network() first.")
            return
        
        print("\n" + "="*60)
        print("SENSOR NETWORK PERFORMANCE ANALYSIS")
        print("="*60)
        
        # Connectivity analysis
        total_sensors = len(self.graph.get_nodes_by_type(NodeType.WEAK))
        connected_sensors = total_sensors - len(self.steiner_solution.unconnected_weak_nodes)
        connectivity_rate = (connected_sensors / total_sensors) * 100
        
        print(f"\nConnectivity Analysis:")
        print(f"  Total sensors: {total_sensors}")
        print(f"  Connected sensors: {connected_sensors}")
        print(f"  Connectivity rate: {connectivity_rate:.1f}%")
        
        # Data hub utilization
        hub_nodes = self.graph.get_nodes_by_type(NodeType.MANDATORY)
        total_hub_capacity = sum(node.capacity for node in hub_nodes)
        used_hub_capacity = sum(
            len(self.graph.get_neighbors(node.id)) 
            for node in hub_nodes 
            if node.id in self.steiner_solution.connected_nodes
        )
        hub_utilization = (used_hub_capacity / total_hub_capacity) * 100 if total_hub_capacity > 0 else 0
        
        print(f"\nData Hub Utilization:")
        print(f"  Total hub capacity: {total_hub_capacity}")
        print(f"  Used capacity: {used_hub_capacity}")
        print(f"  Utilization rate: {hub_utilization:.1f}%")
        
        # Relay node usage
        relay_nodes = self.graph.get_nodes_by_type(NodeType.DISCRETIONARY)
        used_relays = len(self.steiner_solution.used_discretionary_nodes)
        relay_usage_rate = (used_relays / len(relay_nodes)) * 100 if relay_nodes else 0
        
        print(f"\nRelay Node Usage:")
        print(f"  Total relay nodes: {len(relay_nodes)}")
        print(f"  Used relay nodes: {used_relays}")
        print(f"  Usage rate: {relay_usage_rate:.1f}%")
        
        # Network efficiency
        if self.mst_solutions:
            best_mst = min(self.mst_solutions.values(), key=lambda x: x.total_cost)
            efficiency_ratio = self.steiner_solution.total_cost / best_mst.total_cost
            print(f"\nNetwork Efficiency:")
            print(f"  Best MST cost: {best_mst.total_cost:.2f}")
            print(f"  Steiner Tree cost: {self.steiner_solution.total_cost:.2f}")
            print(f"  Efficiency ratio: {efficiency_ratio:.3f}")
        
        # Data collection performance (if data was collected)
        if self.data_collection_history:
            total_data = sum(round_data['total_data'] for round_data in self.data_collection_history)
            avg_transmission_rate = np.mean([round_data['transmission_rate'] 
                                           for round_data in self.data_collection_history])
            
            print(f"\nData Collection Performance:")
            print(f"  Total data collected: {total_data:.1f} KB")
            print(f"  Average transmission rate: {avg_transmission_rate:.1f}%")
            print(f"  Data collection rounds: {len(self.data_collection_history)}")
        
        # Sensor data analysis
        if self.sensor_data:
            print(f"\nSensor Data Analysis:")
            for sensor_id, data_list in self.sensor_data.items():
                avg_data_size = np.mean([d['data_size'] for d in data_list])
                avg_battery = np.mean([d['battery_level'] for d in data_list])
                avg_signal = np.mean([d['signal_strength'] for d in data_list])
                
                print(f"  Sensor {sensor_id}:")
                print(f"    Average data size: {avg_data_size:.1f} KB")
                print(f"    Average battery level: {avg_battery:.1f}%")
                print(f"    Average signal strength: {avg_signal:.2f}")
    
    def visualize_network(self, save_plots: bool = False):
        """Visualize the sensor network and solutions."""
        if not self.graph:
            print("Error: Network not created. Call create_network() first.")
            return
        
        print("\nGenerating visualizations...")
        
        # Plot original network
        self.plotter.plot_network(
            self.graph, 
            title="IoT Sensor Network - Original",
            save_path="sensor_network_original.png" if save_plots else None
        )
        
        # Plot Steiner Tree solution
        if self.steiner_solution:
            self.plotter.plot_steiner_solution(
                self.graph,
                self.steiner_solution,
                title="IoT Sensor Network - Steiner Tree Solution",
                save_path="sensor_network_steiner.png" if save_plots else None
            )
        
        # Plot algorithm comparison
        if self.mst_solutions:
            self.plotter.plot_algorithm_comparison(
                self.graph,
                self.mst_solutions,
                self.steiner_solution,
                title="IoT Sensor Network - Algorithm Comparison",
                save_path="sensor_network_comparison.png" if save_plots else None
            )
        
        # Plot cost comparison
        if self.mst_solutions:
            self.plotter.plot_cost_comparison(
                self.mst_solutions,
                self.steiner_solution,
                title="IoT Sensor Network - Cost Comparison",
                save_path="sensor_network_costs.png" if save_plots else None
            )
    
    def demonstrate_environmental_monitoring(self):
        """Demonstrate environmental monitoring capabilities."""
        print("\n" + "="*60)
        print("ENVIRONMENTAL MONITORING DEMONSTRATION")
        print("="*60)
        
        print("\nEnvironmental Monitoring Applications:")
        print("  1. Air Quality Monitoring")
        print("  2. Temperature and Humidity Tracking")
        print("  3. Noise Level Measurement")
        print("  4. Light Intensity Monitoring")
        print("  5. Motion Detection")
        
        print("\nSensor Network Benefits:")
        print("  - Real-time data collection")
        print("  - Distributed monitoring coverage")
        print("  - Energy-efficient communication")
        print("  - Fault tolerance and redundancy")
        
        # Simulate environmental data collection
        if self.sensor_data:
            print(f"\nSimulated Environmental Data:")
            for sensor_id, data_list in self.sensor_data.items():
                if data_list:  # Check if sensor has data
                    latest_data = data_list[-1]  # Get most recent data
                    print(f"  Sensor {sensor_id}:")
                    print(f"    Data size: {latest_data['data_size']:.1f} KB")
                    print(f"    Battery level: {latest_data['battery_level']:.1f}%")
                    print(f"    Signal strength: {latest_data['signal_strength']:.2f}")
                    print(f"    Transmission cost: {latest_data['transmission_cost']:.2f}")


def main():
    """Main function to run the sensor network system example."""
    print("IoT Sensor Network System")
    print("="*50)
    
    # Create and initialize the system
    system = SensorNetworkSystem()
    
    # Create the network
    system.create_network()
    
    # Optimize the network
    system.optimize_network()
    
    # Analyze network performance
    system.analyze_network_performance()
    
    # Simulate data collection
    system.simulate_data_collection(num_rounds=10)
    
    # Demonstrate environmental monitoring
    system.demonstrate_environmental_monitoring()
    
    # Visualize results
    system.visualize_network(save_plots=True)
    
    print("\nSensor network system example completed successfully!")
    print("Check the generated plots for visual analysis.")


if __name__ == "__main__":
    main()
