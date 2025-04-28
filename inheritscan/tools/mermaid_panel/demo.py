import streamlit as st
from pathlib import Path

import inheritscan
from inheritscan.tools.mermaid_panel.entry import render_mermaid_panel

package_root = Path(inheritscan.__file__).parent

# Streamlit App main
st.set_page_config(page_title="Mermaid Panel", layout="wide")
st.title("📦 Mermaid Panel — Minimum Demo")

with st.container():
    render_mermaid_panel(st)
