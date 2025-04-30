import json
import time
from pathlib import Path

import networkx as nx

import inheritscan

runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"

timeout_seconds = 5
# TODO may need to optimize this timeout logic. The overall goal is to ensure enough time for global_nx_graph to be built.
start_time = time.time()


def _build_subgraph(G: nx.DiGraph, selected_nodes_fpath: str):
    with open(selected_nodes_fpath, "r") as f:
        selected_nodes = json.load(f)

    selected_node_keys = {
        tuple(node["full_mod"].rsplit(".", 1)) for node in selected_nodes
    }

    print(f"\n✅ Selected {len(selected_node_keys)} nodes:")
    for node in selected_node_keys:
        print(f"   - {node}")

    print(f"\n🌐 Inspecting edges from global graph...")

    all_edges = list(G.edges())
    for i, (u, v) in enumerate(all_edges):
        edge_info = f"({u}) -> ({v})"
        match_info = ""
        if u in selected_node_keys and v in selected_node_keys:
            match_info = "✅ MATCH"
            print(f"{i+1:>2}. {edge_info} {match_info}")

    print(f"\n📊 Global Graph: {len(G.nodes)} nodes, {len(G.edges)} edges")

    return G.subgraph(selected_node_keys).copy()


def build_subgraph_from_global(G: nx.DiGraph):
    """
    G: Global Graph
    """
    selected_nodes_fpath = runtime_data_folder / "selected_nodes.json"
    return _build_subgraph(G, selected_nodes_fpath)


def build_detailedgraph_from_subgraph(G: nx.DiGraph):
    """
    G: Sub Graph
    """
    selected_nodes_fpath = runtime_data_folder / "selected_nodes_subgraph.json"
    return _build_subgraph(G, selected_nodes_fpath)
