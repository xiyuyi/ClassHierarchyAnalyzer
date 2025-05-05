from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

# global_graph_demo.py

import streamlit as st

from inheritscan.tools.global_graph import update_global_graph_panel_content

st.set_page_config(page_title="Global Graph Demo", layout="wide")
st.title("🌐 Global Class Graph Panel Demo")

update_global_graph_panel_content()
