"""
Network visualization utilities for IoT networks.

This module provides functions to visualize IoT networks,
algorithm solutions, and comparison results.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Optional, Set
from ..models import IoTGraph, NodeType
from ..algorithms import MSTSolution, SteinerSolution


class NetworkPlotter:
    """Utility class for visualizing IoT networks and solutions."""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """Initialize the network plotter."""
        self.figsize = figsize
        self.colors = {
            NodeType.WEAK: '#FF6B6B',        # Red
            NodeType.MANDATORY: '#4ECDC4',   # Teal
            NodeType.DISCRETIONARY: '#45B7D1'  # Blue
        }
        self.node_sizes = {
            NodeType.WEAK: 300,
            NodeType.MANDATORY: 500,
            NodeType.DISCRETIONARY: 400
        }
    
    def plot_network(self, graph: IoTGraph, title: str = "IoT Network", 
                    show_weights: bool = False, save_path: Optional[str] = None) -> None:
        """
        Plot the IoT network with different node types.
        
        Args:
            graph: The IoT graph to visualize
            title: Title for the plot
            show_weights: Whether to show edge weights
            save_path: Optional path to save the plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Convert to NetworkX for easier plotting
        G = graph.to_networkx()
        
        # Get node positions
        pos = {}
        for node_id in G.nodes():
            node = graph.nodes[node_id]
            if node.position:
                pos[node_id] = node.position
            else:
                # Generate random positions if not specified
                pos[node_id] = (np.random.random(), np.random.random())
        
        # Draw nodes by type
        for node_type in NodeType:
            nodes_of_type = [n for n in G.nodes() 
                            if G.nodes[n]['node_type'] == node_type.value]
            if nodes_of_type:
                nx.draw_networkx_nodes(
                    G, pos, nodelist=nodes_of_type,
                    node_color=self.colors[node_type],
                    node_size=self.node_sizes[node_type],
                    alpha=0.8, ax=ax
                )
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
        
        # Draw edge weights if requested
        if show_weights:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)
        
        # Draw labels
        labels = {n: f"{n}\n({graph.nodes[n].capacity})" 
                for n in G.nodes() if graph.nodes[n].capacity}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)
        
        # Create legend
        legend_elements = [
            patches.Patch(color=self.colors[NodeType.WEAK], label='Weak Nodes'),
            patches.Patch(color=self.colors[NodeType.MANDATORY], label='Mandatory Nodes'),
            patches.Patch(color=self.colors[NodeType.DISCRETIONARY], label='Discretionary Nodes')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        ax.set_title(title)
        ax.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_mst_solution(self, graph: IoTGraph, solution: MSTSolution, 
                         title: str = "MST Solution", save_path: Optional[str] = None) -> None:
        """
        Plot the MST solution on the network.
        
        Args:
            graph: The original IoT graph
            solution: The MST solution to visualize
            title: Title for the plot
            save_path: Optional path to save the plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        G = graph.to_networkx()
        
        # Get node positions
        pos = {}
        for node_id in G.nodes():
            node = graph.nodes[node_id]
            if node.position:
                pos[node_id] = node.position
            else:
                pos[node_id] = (np.random.random(), np.random.random())
        
        # Draw all nodes (light)
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                              node_size=200, alpha=0.3, ax=ax)
        
        # Draw MST edges (thick, colored)
        mst_edges = solution.edges
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, 
                              edge_color='red', width=3, alpha=0.8, ax=ax)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        
        ax.set_title(f"{title}\nCost: {solution.total_cost:.2f}, Algorithm: {solution.algorithm_used}")
        ax.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_steiner_solution(self, graph: IoTGraph, solution: SteinerSolution, 
                              title: str = "Steiner Tree Solution", 
                              save_path: Optional[str] = None) -> None:
        """
        Plot the Steiner Tree solution on the network.
        
        Args:
            graph: The original IoT graph
            solution: The Steiner Tree solution to visualize
            title: Title for the plot
            save_path: Optional path to save the plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        G = graph.to_networkx()
        
        # Get node positions
        pos = {}
        for node_id in G.nodes():
            node = graph.nodes[node_id]
            if node.position:
                pos[node_id] = node.position
            else:
                pos[node_id] = (np.random.random(), np.random.random())
        
        # Draw all nodes (light)
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                              node_size=200, alpha=0.3, ax=ax)
        
        # Draw connected nodes (colored by type)
        for node_type in NodeType:
            connected_of_type = [n for n in solution.connected_nodes 
                               if graph.nodes[n].node_type == node_type]
            if connected_of_type:
                nx.draw_networkx_nodes(
                    G, pos, nodelist=connected_of_type,
                    node_color=self.colors[node_type],
                    node_size=self.node_sizes[node_type],
                    alpha=0.8, ax=ax
                )
        
        # Draw Steiner Tree edges
        nx.draw_networkx_edges(G, pos, edgelist=solution.edges, 
                              edge_color='red', width=3, alpha=0.8, ax=ax)
        
        # Highlight unconnected weak nodes
        unconnected_weak = solution.unconnected_weak_nodes
        if unconnected_weak:
            nx.draw_networkx_nodes(G, pos, nodelist=unconnected_weak,
                                  node_color='black', node_size=300,
                                  alpha=0.5, ax=ax)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        
        # Create legend
        legend_elements = [
            patches.Patch(color=self.colors[NodeType.WEAK], label='Connected Weak'),
            patches.Patch(color=self.colors[NodeType.MANDATORY], label='Mandatory'),
            patches.Patch(color=self.colors[NodeType.DISCRETIONARY], label='Discretionary'),
            patches.Patch(color='black', label='Unconnected Weak')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        ax.set_title(f"{title}\nCost: {solution.total_cost:.2f}, "
                    f"Violations: {solution.capacity_violations}, "
                    f"Unconnected: {len(solution.unconnected_weak_nodes)}")
        ax.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_algorithm_comparison(self, graph: IoTGraph, 
                                 mst_results: Dict[str, MSTSolution],
                                 steiner_solution: Optional[SteinerSolution] = None,
                                 title: str = "Algorithm Comparison",
                                 save_path: Optional[str] = None) -> None:
        """
        Plot comparison of different algorithm results.
        
        Args:
            graph: The original IoT graph
            mst_results: Dictionary of MST algorithm results
            steiner_solution: Optional Steiner Tree solution
            title: Title for the plot
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        G = graph.to_networkx()
        
        # Get node positions
        pos = {}
        for node_id in G.nodes():
            node = graph.nodes[node_id]
            if node.position:
                pos[node_id] = node.position
            else:
                pos[node_id] = (np.random.random(), np.random.random())
        
        # Plot original network
        ax = axes[0]
        for node_type in NodeType:
            nodes_of_type = [n for n in G.nodes() 
                            if G.nodes[n]['node_type'] == node_type.value]
            if nodes_of_type:
                nx.draw_networkx_nodes(
                    G, pos, nodelist=nodes_of_type,
                    node_color=self.colors[node_type],
                    node_size=self.node_sizes[node_type],
                    alpha=0.8, ax=ax
                )
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=6, ax=ax)
        ax.set_title("Original Network")
        ax.axis('off')
        
        # Plot MST solutions
        for i, (alg_name, solution) in enumerate(mst_results.items(), 1):
            if i >= len(axes):
                break
            ax = axes[i]
            
            # Draw all nodes (light)
            nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                                  node_size=150, alpha=0.3, ax=ax)
            
            # Draw MST edges
            nx.draw_networkx_edges(G, pos, edgelist=solution.edges, 
                                  edge_color='red', width=2, alpha=0.8, ax=ax)
            
            nx.draw_networkx_labels(G, pos, font_size=6, ax=ax)
            ax.set_title(f"{alg_name} MST\nCost: {solution.total_cost:.2f}")
            ax.axis('off')
        
        # Plot Steiner solution if available
        if steiner_solution and len(axes) > len(mst_results):
            ax = axes[len(mst_results) + 1]
            
            # Draw all nodes (light)
            nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                                  node_size=150, alpha=0.3, ax=ax)
            
            # Draw connected nodes
            for node_type in NodeType:
                connected_of_type = [n for n in steiner_solution.connected_nodes 
                                   if graph.nodes[n].node_type == node_type]
                if connected_of_type:
                    nx.draw_networkx_nodes(
                        G, pos, nodelist=connected_of_type,
                        node_color=self.colors[node_type],
                        node_size=self.node_sizes[node_type] // 2,
                        alpha=0.8, ax=ax
                    )
            
            # Draw Steiner edges
            nx.draw_networkx_edges(G, pos, edgelist=steiner_solution.edges, 
                                  edge_color='red', width=2, alpha=0.8, ax=ax)
            
            nx.draw_networkx_labels(G, pos, font_size=6, ax=ax)
            ax.set_title(f"Steiner Tree\nCost: {steiner_solution.total_cost:.2f}")
            ax.axis('off')
        
        # Hide unused subplots
        for i in range(len(mst_results) + 2, len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle(title)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_cost_comparison(self, mst_results: Dict[str, MSTSolution],
                           steiner_solution: Optional[SteinerSolution] = None,
                           title: str = "Cost Comparison",
                           save_path: Optional[str] = None) -> None:
        """
        Create a bar chart comparing algorithm costs.
        
        Args:
            mst_results: Dictionary of MST algorithm results
            steiner_solution: Optional Steiner Tree solution
            title: Title for the plot
            save_path: Optional path to save the plot
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data
        algorithms = list(mst_results.keys())
        costs = [solution.total_cost for solution in mst_results.values()]
        
        if steiner_solution:
            algorithms.append("Steiner Tree")
            costs.append(steiner_solution.total_cost)
        
        # Create bar chart
        bars = ax.bar(algorithms, costs, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'][:len(algorithms)])
        
        # Add value labels on bars
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(costs)*0.01,
                   f'{cost:.2f}', ha='center', va='bottom')
        
        ax.set_ylabel('Total Cost')
        ax.set_title(title)
        ax.grid(axis='y', alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
