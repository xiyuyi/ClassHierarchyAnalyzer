import streamlit
import networkx as nx
from pathlib import Path
from inheritscan.tools.mermaid_panel.generate_mermaid_script import get_mermaid_scripts
from inheritscan.tools.mermaid_panel.load_mermaid import load_mermaid_scripts
from inheritscan.tools.mermaid_panel.render import render_mermaid_graph
from inheritscan.tools.uml_panel.render_class_uml import (
    get_detailed_uml_class_graph,
    render_pyvis_class_uml,
)


def render_mermaid_panel(context=None):
    # This is the integration entrypoint for the UML rendering panel in the
    # main Class hierarchy explorer Streamlit app.

    # TODO #7: renders the entire mermaid panel.
    button1 = streamlit.container() # generate mermaid graph
    header = streamlit.container() # header, detailed mermaid graph
    mermaid_graph = streamlit.container() # display mermaid graph
    button2 = streamlit.container() # generate mermaid scripts
    script_box = streamlit.container()
    button3 = streamlit.container() # copy mermaid scripts to clip-board.

    with button1:
        nx_graph = context["detailed_nx_graph"]
        mermaid_script = get_mermaid_scripts(nx_graph)
        print(mermaid_script)
        streamlit.button("Generate Mermaid Graph", use_container_width=True)

    with header:
        streamlit.markdown("### Mermaid Graph:")

    with mermaid_graph:
        # mermaid_scripts = load_mermaid_scripts()
        render_mermaid_graph(mermaid_script)

    with button2:
        streamlit.button("🔁 Generate Mermaid Script", use_container_width=True)

    with script_box:
        streamlit.markdown(" - Here comes the mermaid scripts")

    with button3:
         streamlit.button("📋 Copy Mermaid Script", use_container_width=True)