import streamlit as st
from pyvis.network import Network
from pathlib import Path
import networkx as nx
import tempfile
import os
import json

import inheritscan
package_root = Path(inheritscan.__file__).parent

# -------------------------------
# Mock graph builder
# -------------------------------
def build_mock_class_graph():
    G = nx.DiGraph()
    G = nx.DiGraph()
    G.add_node("CuteCreatur", label=format_class_label("CuteCreaturs", ["eat", "sleep", "PS5"]), is_base=True)
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
    methods_text = "\n".join([f"  {m}()" for m in methods])  # 加两个空格实现左对齐效果
    return f"<class>\n{class_name}\n{line_sep}\n{methods_text}"

# -------------------------------
# Pyvis renderer
# -------------------------------
from pyvis.network import Network
import networkx as nx
import json

def render_pyvis_class_uml(G, font_size=20):
    net = Network(height="650px", width="100%", directed=True)
    
    # Layout tuning for better spacing
    net.repulsion(
        node_distance=100,
        central_gravity=0.2,
        spring_length=200,
        spring_strength=0.05,
        damping=0.95
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
            title=f"{node} class", # this is the hover label
            color={"background": color, "border": "black"},
            font={"size": font_size, "color": "black"},
        )

    # Add edges with clear arrows
    for source, target in G.edges():
        net.add_edge(source, target, arrows="to")

    # Optional: Load external config if you have one
    try:
        with open("umlgraph_pyvis.txt", "r") as f:
            config = json.load(f)
        net.set_options(json.dumps(config))
    except FileNotFoundError:
        pass  # Use defaults if config file is not found

    return net.generate_html()



# -------------------------------
# This is your integration entrypoint!
# -------------------------------
def render_class_uml(metadata=None, context=None):
    st.markdown("### 🗺️ Class Hierarchy Diagram")

    G = build_mock_class_graph()
    html = render_pyvis_class_uml(G)  # now returns HTML string (not file)

    st.components.v1.html(html, height=650, scrolling=True)

    # Sidebar details (still mock)
    st.sidebar.header("Class Details")
    st.sidebar.markdown("**Name:** Dog")
    st.sidebar.markdown("**Description:** Represents a dog, subclass of Animal.")
    st.sidebar.markdown("**Methods:** \n - bark()\n - sleep()")
    st.sidebar.markdown("**Source:** `src/animals/dog.py:10-42`")
    if st.sidebar.button("Jump to VSCode"):
        os.system("code -g src/animals/dog.py:10")


# -------------------------------
# Streamlit App main
# -------------------------------
st.set_page_config(page_title="UML Demao", layout="wide")
st.title("📦 Class Hierarchy Explorer — Minimum Demo")

with st.container():
    render_class_uml()
