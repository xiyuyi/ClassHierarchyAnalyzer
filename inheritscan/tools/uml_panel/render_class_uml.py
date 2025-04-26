from pyvis.network import Network
from pathlib import Path
import networkx as nx
import os
import json
from pyvis.network import Network
import networkx as nx
import json
import inheritscan
from inheritscan.tools.build_detailed_uml_nxg import build_detailed_uml_nx_graph
from inheritscan.tools.extract_subgraph import extract_detailedgraph_from_subgraph, extract_subgraph_from_global
from inheritscan.tools.uml_panel.formats import format_class_label
package_root = Path(inheritscan.__file__).parent
runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"

package_root = Path(inheritscan.__file__).parent

def build_mock_class_graph():
    G = nx.DiGraph()
    G = nx.DiGraph()
    G.add_node(
        "CuteCreatur",
        label=format_class_label("CuteCreaturs", ["eat", "sleep", "PS5"]),
    )
    G.add_node("Dog", label=format_class_label("Dog", ["bark"]))
    G.add_node("XiangXiang", label=format_class_label("XiangXiang", ["PS5"]))
    G.add_node("Cat", label=format_class_label("Cat", ["meow"]))
    G.add_node("Cat1", label=format_class_label("Cat1", ["meow"]))
    G.add_node("Cat2", label=format_class_label("Cat2", ["meow"]))
    G.add_node("Cat3", label=format_class_label("Cat3", ["meow"]))
    G.add_edge("CuteCreatur", "XiangXiang")
    G.add_edge("CuteCreatur", "Dog")
    G.add_edge("CuteCreatur", "Dog")
    G.add_edge("CuteCreatur", "Cat")
    G.add_edge("Cat", "Cat1")
    G.add_edge("Cat", "Cat2")
    G.add_edge("Cat", "Cat3")
    return G


def render_pyvis_class_uml(G: nx.DiGraph, font_size=20):

    # G is the selected nodes for rendering in this panel.
    
    net = Network(height="650px", width="100%", directed=True)
    # Layout tuning for better spacing
    net.repulsion(
        node_distance=800,
        central_gravity=0.01,
        spring_length=200,
        spring_strength=0.05,
        damping=0.95,
    )

    # Define colors
    base_class_color = "#FEB950"
    subclass_color = "#94D841"

    # Add nodes with styling
    for node, data in G.nodes(data=True):
        color = base_class_color if data.get("is_base") else subclass_color
        full_mod = data["full_mod"]
        class_summary = data["class_summary"]
        hover_card = f"{full_mod}\n\n{class_summary}"
        net.add_node(
            node,
            label=data["label"],
            title=hover_card, # this is the content in the card shown with mouse hover.
            shape="box",
            color={"background": color, "border": "black"},
            font={"size": font_size, "color": "black"},
        )

    # Add edges with clear arrows
    for source, target in G.edges():
        net.add_edge(source, target, arrows="to")

    # Load external config
    try:
        with open("umlgraph_pyvis.txt", "r") as f:
            config = json.load(f)
        net.set_options(json.dumps(config))
    except FileNotFoundError:
        pass  # Use defaults if config file is not found

    return net.generate_html()


def get_detailed_uml_class_graph(context) -> nx.DiGraph:
    # get the nx.DiGraph of the subgraph (sub_nx_graph), build from json and global graph
    # TODO the following code block is duplicated with subgraph_render_pyvis_graph. refactor in the future.
    def get_sub_class_hierarchy_network_graph():
        global_nx_graph = context["class_hierachy_network_graph"]
        selected_nodes_from_gg_fpath = runtime_data_folder / "selected_nodes.json"
        sub_nx_graph = extract_subgraph_from_global(global_nx_graph, selected_nodes_from_gg_fpath)
        return sub_nx_graph

    sub_nx_graph: nx.DiGraph = get_sub_class_hierarchy_network_graph()

    # get the  nx.DiGraph for the detailed graph (selection on the subgraph)
    def get_detailed_class_hierarchy_network_graph(sub_nx_graph: nx.DiGraph):
        selected_nodes_from_sg_fpath = runtime_data_folder / "selected_nodes_subgraph.json"
        detailed_nx_graph = extract_detailedgraph_from_subgraph(sub_nx_graph, selected_nodes_from_sg_fpath)
        return detailed_nx_graph
    detailed_nx_graph: nx.DiGraph = get_detailed_class_hierarchy_network_graph(sub_nx_graph)

    # build the nx.DiGraph for detailed uml rendering with the correct labels and names.
    detailed_uml_nx_graph: nx.DiGraph = build_detailed_uml_nx_graph(detailed_nx_graph)
    
    return detailed_uml_nx_graph
    # when test, do the following:
    # return build_mock_class_graph()