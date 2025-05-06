from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

from pathlib import Path

import networkx as nx
from pyvis.network import Network

import inheritscan
from inheritscan.tools.build_subgraph import build_subgraph_from_global
from inheritscan.tools.interactive_pyvis_subgraph import \
    build_interactive_pyvis_subgraph_html
from inheritscan.tools.render_graph import build_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent
runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"


def update_sub_graph_panel_content(context: dict) -> dict:
    log.info("render subgraph")
    return subgraph_get_pyvis_graph_html(context)


def subgraph_get_pyvis_graph_html(context: dict) -> dict:
    log.info("subgraph_get_pyvis_graph_html")
    global_nx_graph = context["class_hierarchy_network_graph"]

    sub_nx_graph: nx.DiGraph = build_subgraph_from_global(global_nx_graph)
    pyvis_subg: Network = build_class_hierarchy_pyvis_network(
        nx_graph=sub_nx_graph, panel="sub_graph"
    )

    # TODO #24 update html block when the render button is clicked
    html = build_interactive_pyvis_subgraph_html(pyvis_subg)
    return {
        "subgraph_class_hierachy_network": sub_nx_graph,
        "interactive_pyvis_subbraph_html": html,
    }
