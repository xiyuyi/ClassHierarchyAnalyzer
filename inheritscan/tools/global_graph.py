import json
from pathlib import Path

import streamlit as st
from pyvis.network import Network

import inheritscan
from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder
from inheritscan.storage.graph_mng import GraphManager
from inheritscan.tools.interactive_pyvisg import interactive_pyvis_graph
from inheritscan.tools.render_graph import get_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent


def render_global_graph_panel(context: dict) -> dict:
    st.markdown("### 🌐 Class Inheritance Graph — Global Graph View")
    return render_pyvis_graph(context)


def render_pyvis_graph(context: dict) -> dict:
    @st.cache_resource
    def get_class_hierarchy_network_graph():
        # TODO #4: expose user input of the initial state info for code base path selection.
        state = {
            "codebase_path": "/Users/xiyuyi/github_repos/OpenHands/openhands",
            "module_cluster_levels": 1,
            "package_name": "openhands",
        }
        builder = ClassHierarchyGraphBuilder()
        class_hierachy_graph = builder.compile_graph()
        state = class_hierachy_graph.invoke(state)

        # TODO housekeeping. need to make this as UI input.
        from inheritscan.storage.runtime_json.runtime_json_dumpers import \
            dump_metadata

        metadata = {"package_name": "openhands"}
        dump_metadata(metadata)

        GraphManager.write_global_graph(state["class_hierarchy_network_graph"])
        return (
            state["class_hierarchy_network_graph"],
            state["modules_name2path"],
            state["modules_details"],
        )

    nx_graph, modules_name2path, modules_details = (
        get_class_hierarchy_network_graph()
    )
    pyvis_g: Network = get_class_hierarchy_pyvis_network(nx_graph)

    pyvis_config_path = package_root / "configs" / "globalgraph_pyvis.txt"
    with open(pyvis_config_path, "r") as f:
        config_json_str = json.dumps(
            json.load(f)
        )  # Pyvis needs str，not dict. json.dumps() converts a dict into tr.
    pyvis_g.set_options(config_json_str)

    interactive_pyvis_graph(pyvis_g)
    return {
        "class_hierarchy_network_graph": nx_graph,
        "modules_name2path": modules_name2path,
        "modules_details": modules_details,
    }


def expand_nodes(nodes):
    # get fqn indexed global class inheritance relation (cir) graph
    cir_g = GraphManager.load_global_graph()

    # get fqn of the selected node
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    meta_fpath = runtime_folder / "meta.json"
    with open(meta_fpath, "r") as f:
        data = json.load(f)
    package_name = data[0]["package_name"]
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
