from pathlib import Path

import streamlit as st
from pyvis.network import Network

import inheritscan
from inheritscan.services.graph_services import \
    get_class_hierarchy_network_graph
from inheritscan.storage.graph_mng import GraphManager
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.interactive_pyvisg import build_interactive_pyvis_graph
from inheritscan.tools.render_graph import build_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent


def render_global_graph_panel(context: dict) -> dict:
    st.markdown("### 🌐 Class Inheritance Graph — Global Graph View")
    return render_pyvis_graph(context)


def render_pyvis_graph(context: dict) -> dict:

    nx_graph, modules_name2path, modules_details = (
        get_class_hierarchy_network_graph()
    )
    pyvis_g: Network = build_class_hierarchy_pyvis_network(
        nx_graph=nx_graph, panel="global_graph"
    )

    # pyvis_config_path = package_root / "configs" / "globalgraph_pyvis.txt"
    # with open(pyvis_config_path, "r") as f:
    #     config_json_str = json.dumps(
    #         json.load(f)
    #     )  # Pyvis needs str，not dict. json.dumps() converts a dict into tr.
    # pyvis_g.set_options(config_json_str)
    print("rendering pyvis_g for global graph")
    html = build_interactive_pyvis_graph(pyvis_g)
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
