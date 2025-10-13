"""
Command-line interface for IoT network optimization.

This module provides a CLI for running network optimization algorithms
and generating visualizations.
"""

import argparse
import sys
import os
from typing import Optional

from .models import IoTGraph
from .algorithms import solve_steiner_tree_constrained, compare_mst_algorithms
from .utils import GraphGenerator, create_sample_networks
from .visualization import NetworkPlotter


def create_network(args) -> IoTGraph:
    """Create a network based on command-line arguments."""
    generator = GraphGenerator(seed=args.seed)
    
    if args.network_type == "random":
        return generator.generate_random_iot_network(
            num_weak=args.num_weak,
            num_mandatory=args.num_mandatory,
            num_discretionary=args.num_discretionary,
            connection_probability=args.connection_prob,
            weight_range=(args.min_weight, args.max_weight),
            capacity_range=(args.min_capacity, args.max_capacity)
        )
    elif args.network_type == "fire":
        return generator.generate_fire_detection_network()
    elif args.network_type == "drone":
        return generator.generate_drone_network()
    elif args.network_type == "grid":
        return generator.generate_grid_iot_network(grid_size=args.grid_size)
    elif args.network_type == "sample":
        networks = create_sample_networks()
        return networks.get(args.sample_name, networks["medium_random"])
    else:
        raise ValueError(f"Unknown network type: {args.network_type}")


def run_optimization(graph: IoTGraph, args) -> dict:
    """Run optimization algorithms on the graph."""
    results = {}
    
    if args.algorithm in ["all", "mst"]:
        print("Running MST algorithms...")
        results["mst"] = compare_mst_algorithms(graph)
    
    if args.algorithm in ["all", "steiner"]:
        print("Running Steiner Tree algorithm...")
        results["steiner"] = solve_steiner_tree_constrained(graph)
    
    return results


def generate_visualizations(graph: IoTGraph, results: dict, args):
    """Generate visualizations for the results."""
    if not args.visualize:
        return
    
    print("Generating visualizations...")
    plotter = NetworkPlotter()
    
    # Plot original network
    plotter.plot_network(graph, title="Original Network")
    
    # Plot MST solutions
    if "mst" in results:
        for name, solution in results["mst"].items():
            plotter.plot_mst_solution(
                graph, solution, 
                title=f"{name} MST Solution"
            )
    
    # Plot Steiner Tree solution
    if "steiner" in results:
        plotter.plot_steiner_solution(
            graph, results["steiner"],
            title="Steiner Tree Solution"
        )
    
    # Plot algorithm comparison
    if "mst" in results and "steiner" in results:
        plotter.plot_algorithm_comparison(
            graph, results["mst"], results["steiner"],
            title="Algorithm Comparison"
        )
        
        plotter.plot_cost_comparison(
            results["mst"], results["steiner"],
            title="Cost Comparison"
        )


def print_results(results: dict):
    """Print optimization results."""
    print("\n" + "="*60)
    print("OPTIMIZATION RESULTS")
    print("="*60)
    
    # MST results
    if "mst" in results:
        print("\nMST Algorithm Results:")
        for name, solution in results["mst"].items():
            print(f"  {name}: Cost = {solution.total_cost:.2f}, "
                  f"Edges = {len(solution.edges)}")
    
    # Steiner Tree results
    if "steiner" in results:
        solution = results["steiner"]
        print(f"\nSteiner Tree Results:")
        print(f"  Total cost: {solution.total_cost:.2f}")
        print(f"  Connected nodes: {len(solution.connected_nodes)}")
        print(f"  Capacity violations: {solution.capacity_violations}")
        print(f"  Unconnected weak nodes: {len(solution.unconnected_weak_nodes)}")
        print(f"  Used discretionary nodes: {len(solution.used_discretionary_nodes)}")
    
    # Best solution
    if "mst" in results and "steiner" in results:
        best_mst = min(results["mst"].values(), key=lambda x: x.total_cost)
        steiner = results["steiner"]
        
        print(f"\nBest Solution:")
        if best_mst.total_cost <= steiner.total_cost:
            print(f"  Algorithm: {best_mst.algorithm_used} MST")
            print(f"  Cost: {best_mst.total_cost:.2f}")
        else:
            print(f"  Algorithm: Steiner Tree")
            print(f"  Cost: {steiner.total_cost:.2f}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="IoT Network Optimization CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all algorithms on a random network
  python -m src.cli --network-type random --algorithm all --visualize
  
  # Run Steiner Tree on fire detection network
  python -m src.cli --network-type fire --algorithm steiner
  
  # Run MST algorithms on sample network
  python -m src.cli --network-type sample --sample-name medium_random --algorithm mst
  
  # Generate grid network with custom parameters
  python -m src.cli --network-type grid --grid-size 8 --algorithm all --visualize
        """
    )
    
    # Network creation arguments
    parser.add_argument(
        "--network-type", 
        choices=["random", "fire", "drone", "grid", "sample"],
        default="random",
        help="Type of network to create"
    )
    
    parser.add_argument(
        "--num-weak", 
        type=int, 
        default=10,
        help="Number of weak nodes (for random networks)"
    )
    
    parser.add_argument(
        "--num-mandatory", 
        type=int, 
        default=3,
        help="Number of mandatory nodes (for random networks)"
    )
    
    parser.add_argument(
        "--num-discretionary", 
        type=int, 
        default=2,
        help="Number of discretionary nodes (for random networks)"
    )
    
    parser.add_argument(
        "--connection-prob", 
        type=float, 
        default=0.4,
        help="Connection probability (for random networks)"
    )
    
    parser.add_argument(
        "--min-weight", 
        type=float, 
        default=1.0,
        help="Minimum edge weight (for random networks)"
    )
    
    parser.add_argument(
        "--max-weight", 
        type=float, 
        default=10.0,
        help="Maximum edge weight (for random networks)"
    )
    
    parser.add_argument(
        "--min-capacity", 
        type=int, 
        default=2,
        help="Minimum node capacity (for random networks)"
    )
    
    parser.add_argument(
        "--max-capacity", 
        type=int, 
        default=5,
        help="Maximum node capacity (for random networks)"
    )
    
    parser.add_argument(
        "--grid-size", 
        type=int, 
        default=4,
        help="Grid size (for grid networks)"
    )
    
    parser.add_argument(
        "--sample-name", 
        type=str, 
        default="medium_random",
        help="Sample network name (for sample networks)"
    )
    
    parser.add_argument(
        "--seed", 
        type=int, 
        default=42,
        help="Random seed for reproducible results"
    )
    
    # Algorithm arguments
    parser.add_argument(
        "--algorithm", 
        choices=["all", "mst", "steiner"],
        default="all",
        help="Algorithm to run"
    )
    
    # Output arguments
    parser.add_argument(
        "--visualize", 
        action="store_true",
        help="Generate visualizations"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Verbose output"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Create network
        print(f"Creating {args.network_type} network...")
        graph = create_network(args)
        
        if args.verbose:
            print(f"Network created:")
            print(f"  Total nodes: {len(graph.nodes)}")
            print(f"  Weak nodes: {len(graph.get_nodes_by_type('weak'))}")
            print(f"  Mandatory nodes: {len(graph.get_nodes_by_type('mandatory'))}")
            print(f"  Discretionary nodes: {len(graph.get_nodes_by_type('discretionary'))}")
            print(f"  Total edges: {len(graph.edges) // 2}")
        
        # Run optimization
        results = run_optimization(graph, args)
        
        # Print results
        print_results(results)
        
        # Generate visualizations
        generate_visualizations(graph, results, args)
        
        print("\nOptimization completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
