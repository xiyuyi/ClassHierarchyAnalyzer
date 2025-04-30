import json
import time
from pathlib import Path

import networkx as nx

import inheritscan

runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"

timeout_seconds = 5
# TODO may need to optimize this timeout logic. The overall goal is to ensure enough time for global_nx_graph to be built.
start_time = time.time()


def build_subgraph(graph, selected_nodes):
    pass


def build_subgraph_from_global(global_nx_graph: nx.DiGraph):
    while not global_nx_graph:
        if time.time() - start_time > timeout_seconds:
            print(
                f"Timeout after {timeout_seconds} seconds waiting for global_nx_graph to be ready."
            )
            break
        time.sleep(0.1)

    print("📦 Loading selected nodes...")

    selected_nodes_from_gg_fpath = runtime_data_folder / "selected_nodes.json"

    with open(selected_nodes_from_gg_fpath, "r") as f:
        selected_nodes = json.load(f)

    selected_node_keys = {
        tuple(node["full_mod"].rsplit(".", 1)) for node in selected_nodes
    }

    print(f"\n✅ Selected {len(selected_node_keys)} nodes:")
    for node in selected_node_keys:
        print(f"   - {node}")

    print(f"\n🌐 Inspecting edges from global graph...")

    all_edges = list(global_nx_graph.edges())
    for i, (u, v) in enumerate(all_edges):
        edge_info = f"({u}) -> ({v})"
        match_info = ""
        if u in selected_node_keys and v in selected_node_keys:
            match_info = "✅ MATCH"
            print(f"{i+1:>2}. {edge_info} {match_info}")

    print(
        f"\n📊 Global Graph: {len(global_nx_graph.nodes)} nodes, {len(global_nx_graph.edges)} edges"
    )

    return global_nx_graph.subgraph(selected_node_keys).copy()


def build_detailedgraph_from_subgraph(sub_nx_graph: nx.DiGraph):
    while not sub_nx_graph:
        if time.time() - start_time > timeout_seconds:
            print(
                f"Timeout after {timeout_seconds} seconds waiting for sub_nx_graph to be ready."
            )
            break
        time.sleep(0.1)

    print("📦 Loading selected nodes from subgraph...")

    selected_nodes_from_sb_fpath = (
        runtime_data_folder / "selected_nodes_subgraph.json"
    )
    with open(selected_nodes_from_sb_fpath, "r") as f:
        selected_nodes = json.load(f)

    selected_node_keys = {
        tuple(node["full_mod"].rsplit(".", 1)) for node in selected_nodes
    }

    print(f"\n✅ Selected {len(selected_node_keys)} nodes:")
    for node in selected_node_keys:
        print(f"   - {node}")

    print(f"\n🌐 Inspecting edges from global graph...")

    all_edges = list(sub_nx_graph.edges())
    for i, (u, v) in enumerate(all_edges):
        edge_info = f"({u}) -> ({v})"
        match_info = ""
        if u in selected_node_keys and v in selected_node_keys:
            match_info = "✅ MATCH"
            print(f"{i+1:>2}. {edge_info} {match_info}")

    print(
        f"\n📊 Global Graph: {len(sub_nx_graph.nodes)} nodes, {len(sub_nx_graph.edges)} edges"
    )

    return sub_nx_graph.subgraph(selected_node_keys).copy()
