from inheritscan.tools.global_graph import render_global_graph_panel


def render_top_left(context:dict, streamlit):
    result = render_global_graph_panel(context)
    if result:
        streamlit.session_state.update(result)