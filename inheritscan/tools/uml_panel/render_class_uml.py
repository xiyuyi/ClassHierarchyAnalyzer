from pyvis.network import Network
from pathlib import Path
import networkx as nx
import os
import json
from pyvis.network import Network
import networkx as nx
import json
import inheritscan

package_root = Path(inheritscan.__file__).parent

def build_mock_class_graph():
    G = nx.DiGraph()
    G = nx.DiGraph()
    G.add_node(
        "CuteCreatur",
        label=format_class_label("CuteCreaturs", ["eat", "sleep", "PS5"]),
        is_base=True,
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


def format_class_label(class_name, methods):
    line_sep = "------------------"
    methods_text = "\n".join([f"  {m}()" for m in methods])
    return f"<class>\n{class_name}\n{line_sep}\n{methods_text}"


def render_pyvis_class_uml(G: nx.DiGraph, font_size=20):
    # G is the selected nodes for rendering in this panel.
    net = Network(height="650px", width="100%", directed=True)
    # Layout tuning for better spacing
    net.repulsion(
        node_distance=100,
        central_gravity=0.2,
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
        net.add_node(
            node,
            label=data["label"],
            shape="box",
            title=f"{node} class",  
            # TODO #7 this is the hover label, should change to more detailed version.
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


def get_detailed_uml_class_graph():
    # TODO #7 in real app, replace with the real graph builder
    return build_mock_class_graph()
