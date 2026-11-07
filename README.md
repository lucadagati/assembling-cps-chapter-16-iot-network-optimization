# IoT Network Optimization — MST and constrained Steiner Tree

Python implementation of the algorithms of **Chapter 16 ("IoT-driven peer-to-peer networking")** of the book *Assembling Smart Cyber-Physical Systems: heterogeneous, diffuse and green technological infrastructures for cities and industries*. It lets you build synthetic IoT networks, connect them with classical **Minimum Spanning Tree** algorithms (Kruskal, Prim, degree-constrained Prim) or with a **capacity-constrained Steiner Tree** heuristic, and compare cost, connectivity and capacity violations.

## 1. The problem in a nutshell

IoT devices must be interconnected at minimum communication cost while staying fully connected. A plain MST ignores real constraints — a sensor can serve only a few links, some devices *must* take part and others are optional relays — and may therefore be unusable. The model has three kinds of nodes:

| Node type | Meaning | Capacity (max links) | In generated networks |
|---|---|---|---|
| **Weak** | battery sensor that must be connected, cannot relay | 1 | `capacity=1` |
| **Mandatory** | always part of the network, acts as relay/gateway | limited | random in `capacity_range` (default 2–5) |
| **Discretionary** | optional hub, used only if it lowers the objective | limited | random in `capacity_range` |

The Steiner solver connects every weak node to the mandatory backbone through the cheapest feasible path (optionally through discretionary nodes), counts **capacity violations**, lists **unconnected weak nodes** and scores the result with a weighted combination of average connection cost (ACC) and average operation cost (AOC). Background and derivations are in [docs/theory/](docs/theory/) and [docs/algorithms/implementation_guide.md](docs/algorithms/implementation_guide.md).

## 2. Requirements and installation

Python 3.8+ (tested with 3.10). Core dependencies are only `numpy`, `networkx`, `matplotlib` and `pytest`.

```bash
git clone https://github.com/lucadagati/assembling-cps-chapter-16-iot-network-optimization.git
cd assembling-cps-chapter-16-iot-network-optimization
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# optional: dashboards/notebooks/extra plotting
pip install -r requirements-extras.txt
```

Run everything from the repository root (the package is imported as `src`). On a machine without a display set `export MPLBACKEND=Agg` before running scripts that plot.

## 3. Quick start (command line)

```bash
python -m src.cli --help
python -m src.cli --network-type random --num-weak 6 --seed 1 --algorithm all
```

Output (deterministic for a given `--seed`):

```
MST Algorithm Results:
  Kruskal: Cost = 30.60, Edges = 10
  Prim: Cost = 30.60, Edges = 10
  ConstrainedPrim: Cost = 6.87, Edges = 3

Steiner Tree Results:
  Total cost: 22.09
  Connected nodes: 10
  Capacity violations: 1
  Unconnected weak nodes: 1
  Used discretionary nodes: 2

Best Solution:
  Algorithm: Steiner Tree
  Cost: 22.09
```

How to read it: a spanning tree on 11 nodes has 10 edges, so Kruskal/Prim span the whole network. `ConstrainedPrim` honours node capacities but, with tight limits, only builds a *forest* (3 edges) — its low cost is **not comparable** with a spanning tree, which is why "best solution" selection (`select_best_mst`) prefers solutions that connect more nodes before comparing cost.

Useful options: `--network-type {random,fire,drone,grid,sample}`, `--num-weak/--num-mandatory/--num-discretionary`, `--connection-prob`, `--min-weight/--max-weight`, `--min-capacity/--max-capacity`, `--grid-size`, `--sample-name {simple,medium,large,disconnected,capacity_constrained}`, `--algorithm {all,mst,steiner}`, `--seed`, `--visualize` (opens/saves plots), `--verbose`.

## 4. Using it as a library

```python
from src.algorithms import solve_steiner_tree_constrained, compare_mst_algorithms, select_best_mst
from src.utils import GraphGenerator

graph = GraphGenerator(seed=42).generate_random_iot_network(
    num_weak=10, num_mandatory=3, num_discretionary=2)   # always connected

steiner = solve_steiner_tree_constrained(graph)
print(steiner)                       # cost, connected nodes, violations, unconnected weak nodes
print(steiner.get_score(alpha=0.5))  # objective function value

mst = compare_mst_algorithms(graph)  # {"Kruskal": ..., "Prim": ..., "ConstrainedPrim": ...}
for name, sol in mst.items():
    print(name, round(sol.total_cost, 2), len(sol.edges), "edges")
print("best MST:", select_best_mst(mst.values()))
```

Main classes: `IoTGraph`/`Node`/`Edge`/`NodeType` (`src/models/graph.py`), `KruskalMST`, `PrimMST`, `ConstrainedMST` (`src/algorithms/mst.py`), `GreedySteinerTree` and `solve_steiner_tree_constrained` (`src/algorithms/steiner_tree.py`), `GraphGenerator` (random/grid/fire/drone networks) and the ready-made graphs in `data/sample_networks.py`.

## 5. Worked examples

Three application scenarios, each a self-contained script that builds a network, runs all algorithms, prints an analysis and writes four PNG plots (original network, comparison, costs, Steiner tree) into the current directory:

| Script | Scenario | Example result (seed fixed in script) |
|---|---|---|
| `examples/fire_detection/fire_detection_system.py` | 20 sensors, 2 supply nodes, 2 hubs | Steiner cost 41.27, 2 unconnected sensors; Kruskal/Prim 34.95 on 23 edges |
| `examples/drone_network/drone_coordination.py` | drone swarm coordination | see script output |
| `examples/iot_sensors/sensor_network.py` | environmental sensor field | see script output |

```bash
export MPLBACKEND=Agg
mkdir -p out && cd out
PYTHONPATH=.. python ../examples/fire_detection/fire_detection_system.py
# or everything at once from the repository root:
python run_examples.py
```

## 6. Tests

```bash
python -m pytest -q tests        # 19 tests: MST, Steiner, graph model, integration
python run_tests.py              # same, with timing summary
```

## 7. Reproducibility notes

- All generators take a `seed`; the CLI exposes `--seed`. Identical seeds give identical networks and results.
- Generated random networks are **forced to be connected** (components are bridged through non-weak nodes), so Kruskal/Prim always return `|V|-1` edges.
- Results above were produced with Python 3.10, numpy 2.2, networkx 3.4.

## 8. Repository layout

```
src/
  models/          IoTGraph, Node, Edge, NodeType
  algorithms/      mst.py (Kruskal, Prim, ConstrainedMST, select_best_mst), steiner_tree.py
  utils/           GraphGenerator (random, grid, fire, drone networks)
  visualization/   NetworkPlotter (network, comparison and cost plots)
  cli.py           command-line interface
examples/          fire_detection/, drone_network/, iot_sensors/
data/              sample networks used by tests and the CLI
tests/             unit and integration tests
docs/              theory/, algorithms/, examples/ (Markdown)
run_examples.py, run_tests.py, setup.py, requirements*.txt
```

## 9. Known limitations

- The Steiner solver is a greedy heuristic: it is not guaranteed optimal and may leave weak nodes unconnected or violate capacities when the instance is tight (both are reported).
- `ConstrainedMST` is a degree-limited Prim heuristic; with strict limits it returns a forest rather than a spanning tree.
- Networks are synthetic; no real topology import is provided.

## 10. Changes in this revision

Fixed: Kruskal dropped edges stored with `source > target`; `SteinerSolution.get_score` crashed (no graph reference); `PrimMST` failed on empty graphs; `ConstrainedMST` ignored the source node's degree limit; random networks could be disconnected; the comparison plot crashed with an Steiner panel; `setup.py` placeholders; heavy optional dependencies (`pygraphviz`, `dash`, ...) moved to `requirements-extras.txt`. See [CHANGELOG.md](CHANGELOG.md).

## Citation

If you use this code in your research, please cite:

```
Chapter 16: IoT-driven peer-to-peer networking
In: "Assembling Smart Cyber-Physical Systems: heterogeneous, diffuse and green technological infrastructures for cities and industries"
Authors: Prof. Giuseppe Tricomi, Prof. Pasquale De Meo, Dr. Marco Garofalo
```
