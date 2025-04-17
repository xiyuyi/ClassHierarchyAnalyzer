import random
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import tempfile
import numpy as np
from collections import deque

from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder
from inheritscan.tools.interactive_pyvisg import interactive_pyvis_graph
from inheritscan.tools.mock_graphs import get_mock_graph, get_mock_graph_class_inheritance
from inheritscan.tools.radial_tree import radial_tree_layout
from inheritscan.tools.render_graph import get_class_hierarchy_pyvis_network


def render_global_graph_panel(context: dict) -> dict:
    st.markdown("### 🌐 Global Class Graph")
    return render_pyvis_graph(context)


def render_pyvis_graph(context: dict) -> dict:
    st.markdown(" Pyvis Graph View")

    physics_enabled = st.checkbox("Enable physics layout (force-based radial)", value=True)
    # disable_after_stabilization = st.checkbox("Disable physics after layout stabilization", value=True)

    # nx_graph = get_mock_graph(num_nodes=1000)
    @st.cache_resource
    def get_class_hierarchy_network_graph():
        # 1. Initialize state
        state = {
            'codebase_path': '/Users/xiyuyi/github_repos/OpenHands/openhands',
            'module_cluster_levels': 1,
            'package_name': 'openhands'
        }
        builder = ClassHierarchyGraphBuilder()
        class_hierachy_graph = builder.compile_graph()
        state = class_hierachy_graph.invoke(state)
        return state['class_hierachy_network_graph']

    nx_graph = get_class_hierarchy_network_graph()
    pyvis_g = get_class_hierarchy_pyvis_network(nx_graph)
    # nx_graph = get_mock_graph_class_inheritance(num_nodes=1000)
    # G = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")

    # pos = radial_tree_layout(nx_graph)
    # for node in nx_graph.nodes(data=True):
    #     mod = node[1].get("module", "core")
    #     color = {"core": "blue", "vision": "red", "nlp": "orange", "audio": "green", "root": "black"}.get(mod, "gray")
    #     x, y = pos.get(node[0], (0, 0))
    #     G.add_node(node[0], title=f"Module: {mod}", color=color, x=x, y=y)
    # pos = radial_tree_layout(nx_graph)
    # print("adding nodes")
    # for node in nx_graph.nodes(data=True):
    #     print(node)
    #     mod = node[1].get("class_name", "EMPTY")
    #     print(mod)
    #     print(type(node[0]))
    #     G.add_node(node[0][1], title=mod)
    
    # print("adding nodes")
    # for node in nx_graph.nodes(data=True):
    #     mod = node[0][1]
    #     print(mod)
    #     print(node)
    #     G.add_node(node, title=mod)

    # for edge in nx_graph.edges():
    #     print(edge)
    #     G.add_edge(edge[0][1], edge[1][1])

    if physics_enabled:
        pyvis_g.set_options('''{
        "layout": { "hierarchical": { "enabled": false } },
        "physics": {
            "enabled": true,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
            "gravitationalConstant": -50,
            "centralGravity": 0.002,
            "springLength": 10,
            "springConstant": 0.2,
            "avoidOverlap": 1
            },
            "minVelocity": 1.0,
            "timestep": 0.2,
            "stabilization": {
            "enabled": true,
            "iterations": 150,
            "updateInterval": 10,
            "fit": false
            }
        }
        }''')


    # with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
    #     pyvis_g.save_graph(tmp.name)
    #     html = open(tmp.name, 'r', encoding='utf-8').read()
    #     components.html(html, height=600, scrolling=True)

    selected_node = interactive_pyvis_graph(pyvis_g)
    return {"selected_cluster": selected_node}





