import streamlit
import networkx as nx
from pathlib import Path
from inheritscan.tools.uml_panel.render_class_uml import (
    get_detailed_uml_class_graph,
    render_pyvis_class_uml,
)


def render_class_uml(context=None):
    # This is the integration entrypoint for the UML rendering panel in the
    # main Class hierarchy explorer Streamlit app.

    # TODO #7: render detailed UML diagram for the selected classes.
    # with basic summaries displayed with mouse hover event on each node.
    # modify the node's labels for information to be displayed with mouse hover event.

    # TODO #7
    # load nodes information from .run_time/selected_nodes_subgraph.json
    # calculate/retrieve the detailed information for this cluster of nodes
    # save out to .run_time/detailed_uml_info.json
    # Information should be:
    # Aggregate class summaries (class leve, method level, chunks level, everything), and inheritance info.
    # enough to generate diagrams
    # enough to generate mermaid or plantuml codes (need inheritanc einformation?)

    nx_graph: nx.DiGraph = get_detailed_uml_class_graph(context)
    html = render_pyvis_class_uml(nx_graph)

    # Read the JS content
    current_script_path = Path(__file__).parent.resolve()
    js_file_path = current_script_path / "node_selection_event_listener.js"
    with open(js_file_path, "r") as f:
        js_code = f.read()
    script_block = f"\n<script type='text/javascript'>\n{js_code}\n</script>\n"

    # Append it to the end of the html string, this way selected nodes would be saved to .json file
    # the .json file would be used in the bottom right panel for detailed information display.
    html += script_block

    # render
    streamlit.components.v1.html(html, height=650, scrolling=True)
