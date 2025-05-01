from pathlib import Path

from pyvis.network import Network

import inheritscan
from inheritscan.services.graph_services import \
    get_class_hierarchy_network_graph
from inheritscan.storage.graph_mng import GraphManager
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.interactive_pyvisg import \
    build_interactive_pyvis_graph_html
from inheritscan.tools.render_graph import build_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent


def update_global_graph_panel_content(context: dict) -> dict:
    return get_globalgraph_pyvis_html(context)


def get_globalgraph_pyvis_html(context: dict) -> dict:

    nx_graph, modules_name2path, modules_details = (
        get_class_hierarchy_network_graph()
    )
    pyvis_g: Network = build_class_hierarchy_pyvis_network(
        nx_graph=nx_graph, panel="global_graph"
    )

    print("rendering pyvis_g for global graph")
    html = build_interactive_pyvis_graph_html(pyvis_g)
    return {
        "class_hierarchy_network_graph": nx_graph,
        "modules_name2path": modules_name2path,
        "modules_details": modules_details,
        "interactive_pyvis_global_graph_html": html,
    }


def expand_nodes(nodes):
    # get fqn indexed global class inheritance relation (cir) graph
    cir_g = GraphManager.load_global_graph()

    # get fqn of the selected node
    data = load_metadata()
    package_name = data["package_name"]
    fqn = package_name + "." + nodes[0]["full_mod"]

    # get children of the selected node
    children = cir_g[fqn]

    for child in children:
        full_mod = child.split(".", 1)[1]
        id = full_mod.rsplit(".", 1)[1]
        entry = {
            "id": id,
            "full_mod": full_mod,
        }
        nodes.append(entry)

    return nodes
