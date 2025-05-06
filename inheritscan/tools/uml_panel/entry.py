from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

from pathlib import Path

import streamlit

from inheritscan.tools.uml_panel.render_class_uml import (
    get_detailed_uml_class_graph, render_pyvis_class_uml)


def render_class_uml(context=None):
    """This is the integration entrypoint for the UML rendering panel"""

    result = get_detailed_uml_class_graph(context)
    nx_graph, detailed_nx_graph = result  # here nx_graph is a DiGraph
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
    return {
        "detailed_uml_class_graph": nx_graph,
        "detailed_nx_graph": detailed_nx_graph,
    }
