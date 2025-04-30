from pathlib import Path

import networkx as nx
from pyvis.network import Network

import inheritscan
from inheritscan.tools.build_subgraph import build_subgraph_from_global
from inheritscan.tools.interactive_pyvis_subgraph import \
    get_interactive_pyvis_subgraph_html
from inheritscan.tools.render_graph import build_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent
runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"


def render_sub_graph_panel(context: dict) -> dict:
    print("render subgraph")
    return subgraph_render_pyvis_graph(context)


def subgraph_render_pyvis_graph(context: dict) -> dict:
    print("subgraph_render_pyvis_graph")

    sub_nx_graph: nx.DiGraph = get_sub_class_hierarchy_network_graph(context)
    pyvis_subg: Network = build_class_hierarchy_pyvis_network(
        nx_graph=sub_nx_graph, panel="sub_graph"
    )

    # TODO #24 update html block when the render button is clicked
    html = get_interactive_pyvis_subgraph_html(pyvis_subg)
    return {
        "subgraph_class_hierachy_network": sub_nx_graph,
        "interactive_pyvis_subbraph_html": html,
    }


def get_sub_class_hierarchy_network_graph(context):
    global_nx_graph = context["class_hierarchy_network_graph"]
    selected_nodes_from_gg_fpath = runtime_data_folder / "selected_nodes.json"
    sub_nx_graph = build_subgraph_from_global(
        global_nx_graph, selected_nodes_from_gg_fpath
    )
    return sub_nx_graph
