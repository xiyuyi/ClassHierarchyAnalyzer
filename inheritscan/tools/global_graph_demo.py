# global_graph_demo.py

import streamlit as st

from inheritscan.tools.global_graph import render_global_graph_panel

st.set_page_config(page_title="Global Graph Demo", layout="wide")
st.title("🌐 Global Class Graph Panel Demo")

render_global_graph_panel()
