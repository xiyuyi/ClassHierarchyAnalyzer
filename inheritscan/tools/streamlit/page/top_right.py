import streamlit

from inheritscan.tools.sub_graph import render_sub_graph_panel


def render_top_right(context):
    streamlit.markdown("### 🔍 Class Inheritance Graph — Subgraph View")

    # button to trigger subgraph rendering
    if streamlit.button("🔁 Render Subgraph", use_container_width=True):
        streamlit.session_state["rerender_subgraph"] = True
        result = render_sub_graph_panel(context)
        if result:
            streamlit.session_state.update(result)

    # window area for the graph rendering
    subgraph_container = streamlit.container()
    with subgraph_container:

        # retrieve the html with ineractive selection logic for the panel.
        html = streamlit.session_state.interactive_pyvis_subbraph_html

        # render with the modified html.
        streamlit.components.v1.html(html, height=500, scrolling=True)
        streamlit.session_state["rerender_subgraph"] = False
