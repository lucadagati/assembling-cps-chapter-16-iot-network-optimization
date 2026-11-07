"""
Setup script for IoT Network Optimization Package.

This package implements algorithms for optimizing IoT network connectivity
including Minimum Spanning Tree and constrained Steiner Tree algorithms.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="iot-network-optimization",
    version="1.0.0",
    author="Luca D'Agati",
    description="IoT network optimization algorithms for heterogeneous device connectivity",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/lucadagati/assembling-cps-chapter-16-iot-network-optimization",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "iot-network-optimize=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="iot, network, optimization, mst, steiner-tree, graph-theory, algorithms",
    project_urls={
        "Bug Reports": "https://github.com/lucadagati/assembling-cps-chapter-16-iot-network-optimization/issues",
        "Source": "https://github.com/lucadagati/assembling-cps-chapter-16-iot-network-optimization",
    },
)
