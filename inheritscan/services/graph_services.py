import streamlit

from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder
from inheritscan.storage.graph_mng import GraphManager
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.get_graph_state import build_graph_state_from_metadata


@streamlit.cache_resource
def get_class_hierarchy_network_graph():
    # retrieve metadata, and copy over to
    metadata = load_metadata()
    state = build_graph_state_from_metadata(metadata)

    # use langchain graph to get class hiearchy network graph
    builder = ClassHierarchyGraphBuilder()
    class_hierachy_graph = builder.compile_graph()
    state = class_hierachy_graph.invoke(state)

    # write graph to file
    GraphManager.write_global_graph(state["class_hierarchy_network_graph"])
    return (
        state["class_hierarchy_network_graph"],
        state["modules_name2path"],
        state["modules_details"],
    )
