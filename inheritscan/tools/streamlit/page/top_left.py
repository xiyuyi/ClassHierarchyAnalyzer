import streamlit

from inheritscan.tools.global_graph import render_global_graph_panel


def render_top_left(context: dict):
    result = render_global_graph_panel(context)
    if result:
        streamlit.session_state.update(result)

    # Display and return selected node from Streamlit frontend
    html = streamlit.session_state.interactive_pyvis_global_graph_html
    streamlit.components.v1.html(html, height=500, scrolling=True)
