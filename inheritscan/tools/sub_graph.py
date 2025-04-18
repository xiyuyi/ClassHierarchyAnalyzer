from pyvis.network import Network
from collections import deque
from pathlib import Path

import streamlit as st
import json
import inheritscan

from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder
from inheritscan.tools.extract_subgraph import extract_subgraph_from_global
from inheritscan.tools.interactive_pyvis_subgraph import interactive_pyvis_subgraph
from inheritscan.tools.interactive_pyvisg import interactive_pyvis_graph
from inheritscan.tools.mock_graphs import get_mock_graph, get_mock_graph_class_inheritance
from inheritscan.tools.radial_tree import radial_tree_layout
from inheritscan.tools.render_graph import get_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent
runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"

def render_sub_graph_panel(context: dict) -> dict:
    print("render subgraph")
    return subgraph_render_pyvis_graph(context)


def subgraph_render_pyvis_graph(context: dict) -> dict:
    print("subgraph_render_pyvis_graph")
    # physics_enabled = st.checkbox("Enable physics layout for subgraph (force-based radial)", value=True)

    
    def get_sub_class_hierarchy_network_graph():
        global_nx_graph = context["class_hierachy_network_graph"]
        selected_nodes_from_gg_fpath = runtime_data_folder / "selected_nodes.json"
        sub_nx_graph = extract_subgraph_from_global(global_nx_graph, selected_nodes_from_gg_fpath)
        return sub_nx_graph

    sub_nx_graph = get_sub_class_hierarchy_network_graph()
    pyvis_subg = get_class_hierarchy_pyvis_network(sub_nx_graph)


    pyvis_config_path = package_root / "configs" / "subgraph_pyvis.txt"
    with open(pyvis_config_path, "r") as f:
        config_json_str = json.dumps(json.load(f))  
    pyvis_subg.set_options(config_json_str)

    selected_node = interactive_pyvis_subgraph(pyvis_subg)
    return {"subgraph_class_hierachy_network": sub_nx_graph}

