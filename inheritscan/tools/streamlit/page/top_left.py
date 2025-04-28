from inheritscan.tools.global_graph import render_global_graph_panel
import streamlit

def render_top_left(context:dict):
    result = render_global_graph_panel(context)
    if result:
        streamlit.session_state.update(result)