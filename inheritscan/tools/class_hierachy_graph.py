import streamlit as st

from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder


@st.cache_resource
def get_class_hierarchy_network_graph():
    # 1. Initialize state
    state = {
        "codebase_path": "/Users/xiyuyi/github_repos/OpenHands/openhands",
        "module_cluster_levels": 1,
        "package_name": "openhands",
    }
    builder = ClassHierarchyGraphBuilder()
    class_hierachy_graph = builder.compile_graph()
    state = class_hierachy_graph.invoke(state)
    return state["class_hierarchy_network_graph"]
