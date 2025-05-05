from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import streamlit

from inheritscan.tools.global_graph import update_global_graph_panel_content


def render_top_left(context: dict):
    # define layout
    header = streamlit.container()
    graph_display = streamlit.container()

    # render components:
    with header:
        streamlit.markdown(
            "### 🌐 Class Inheritance Graph — Global Graph View"
        )

    with graph_display:
        # Display and return selected node from Streamlit frontend
        html = streamlit.session_state.get(
            "interactive_pyvis_global_graph_html", ""
        )
        streamlit.components.v1.html(html, height=500, scrolling=True)

    # define actions
    result = update_global_graph_panel_content(context)
    if result:
        streamlit.session_state.update(result)
