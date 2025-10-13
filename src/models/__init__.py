"""
Data models for IoT network optimization.

This package contains the core data structures used throughout
the IoT network optimization algorithms.
"""

from .graph import NodeType, Node, Edge, IoTGraph

__all__ = ['NodeType', 'Node', 'Edge', 'IoTGraph']
