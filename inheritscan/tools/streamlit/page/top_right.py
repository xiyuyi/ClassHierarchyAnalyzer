import streamlit

from inheritscan.tools.sub_graph import render_sub_graph_panel


def render_top_right(context):
    streamlit.markdown("### 📎 Subgraph View")

    # Button always stays fixed
    if streamlit.button("🔁 Render Subgraph", use_container_width=True):
        streamlit.session_state["rerender_subgraph"] = True

    # Render area isolated from button
    subgraph_container = streamlit.container()
    with subgraph_container:
        if streamlit.session_state.get("rerender_subgraph", True):
            result = render_sub_graph_panel(context)
            if result:
                streamlit.session_state.update(result)
