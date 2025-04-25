from pyvis.network import Network
from collections import deque
from pathlib import Path

import streamlit as st
import json
import inheritscan

from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder
from inheritscan.tools.interactive_pyvisg import interactive_pyvis_graph
from inheritscan.tools.mock_graphs import get_mock_graph, get_mock_graph_class_inheritance
from inheritscan.tools.radial_tree import radial_tree_layout
from inheritscan.tools.render_graph import get_class_hierarchy_pyvis_network

package_root = Path(inheritscan.__file__).parent

def render_global_graph_panel(context: dict) -> dict:
    st.markdown("### 🌐 Global Class Graph")
    return render_pyvis_graph(context)


def render_pyvis_graph(context: dict) -> dict:
    st.markdown(" Pyvis Graph View")

    physics_enabled = st.checkbox("Enable physics layout (force-based radial)", value=True)

    @st.cache_resource
    def get_class_hierarchy_network_graph():
        # TODO #4: expose user input of the initial state info for code base path selection.
        state = {
            'codebase_path': '/Users/xiyuyi/github_repos/OpenHands/openhands',
            'module_cluster_levels': 1,
            'package_name': 'openhands'
        }
        builder = ClassHierarchyGraphBuilder()
        class_hierachy_graph = builder.compile_graph()
        state = class_hierachy_graph.invoke(state)
        return state['class_hierachy_network_graph'], state['modules_name2path'], state['modules_details']

    nx_graph, modules_name2path, modules_details = get_class_hierarchy_network_graph()
    pyvis_g: Network = get_class_hierarchy_pyvis_network(nx_graph)


    pyvis_config_path = package_root / "configs" / "globalgraph_pyvis.txt"
    with open(pyvis_config_path, "r") as f:
        config_json_str = json.dumps(json.load(f))  # Pyvis needs str，not dict. json.dumps() converts a dict into tr.
    pyvis_g.set_options(config_json_str)

    interactive_pyvis_graph(pyvis_g)
    return {"class_hierachy_network_graph": nx_graph, 
            "modules_name2path": modules_name2path,
            "modules_details": modules_details}





