from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import os
from pathlib import Path

import streamlit as st

import inheritscan
from inheritscan.tools.uml_panel.entry import render_class_uml

package_root = Path(inheritscan.__file__).parent

# -------------------------------
# Streamlit App main
# -------------------------------
st.set_page_config(page_title="UML Demao", layout="wide")
st.title("📦 Class Hierarchy Explorer — Minimum Demo")

with st.container():
    render_class_uml(st)
    # Sidebar details (still mock)
    st.sidebar.header("Class Details")
    st.sidebar.markdown("**Name:** Dog")
    st.sidebar.markdown(
        "**Description:** Represents a dog, subclass of Animal."
    )
    st.sidebar.markdown("**Methods:** \n - bark()\n - sleep()")
    st.sidebar.markdown("**Source:** `src/animals/dog.py:10-42`")
    if st.sidebar.button("Jump to VSCode"):
        os.system("code -g src/animals/dog.py:10")
