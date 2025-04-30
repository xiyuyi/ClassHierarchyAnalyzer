import streamlit

from inheritscan.tools.sub_graph import render_sub_graph_panel


def render_top_right(context):
    streamlit.markdown("### 🔍 Class Inheritance Graph — Subgraph View")

    # button to trigger subgraph rendering
    if streamlit.button("🔁 Render Subgraph", use_container_width=True):
        streamlit.session_state["rerender_subgraph"] = True

    # window area for the graph rendering
    subgraph_container = streamlit.container()
    with subgraph_container:
        if streamlit.session_state.get("rerender_subgraph", True):
            result = render_sub_graph_panel(context)
            if result:
                streamlit.session_state.update(result)
            streamlit.session_state["rerender_subgraph"] = False
