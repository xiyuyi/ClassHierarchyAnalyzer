import streamlit

from inheritscan.tools.sub_graph import update_sub_graph_panel_content


def render_top_right(context):
    # define layout:
    header = streamlit.container()
    button1 = streamlit.container()
    graph_display = streamlit.container()

    # render each component
    with header:
        streamlit.markdown("### 🔍 Class Inheritance Graph — Subgraph View")

    with button1:
        # button to trigger subgraph rendering
        b1_handle = streamlit.button(
            "🔁 Render Subgraph", use_container_width=True
        )

    with graph_display:
        # retrieve the html with ineractive selection logic for the panel.
        html = streamlit.session_state.get(
            "interactive_pyvis_subbraph_html", ""
        )
        # render with the modified html.
        streamlit.components.v1.html(html, height=500, scrolling=True)
        streamlit.session_state["rerender_subgraph"] = False

    # define actions
    if b1_handle:
        streamlit.session_state.rerender_subgraph = True
        result = update_sub_graph_panel_content(context)
        if result:
            streamlit.session_state.update(result)
