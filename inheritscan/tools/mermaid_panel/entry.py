from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import streamlit as st

from inheritscan.tools.mermaid_panel.generate_mermaid_script import \
    get_mermaid_scripts
from inheritscan.tools.mermaid_panel.render import render_mermaid_graph


def render_mermaid_panel(context=None):
    # Integration entrypoint for the UML rendering panel in the Class Hierarchy Explorer app

    # Define high-level containers
    button1 = st.container()
    header = st.container()
    mermaid_graph = st.container()
    script_box = st.container()

    # Create a session state to store the generated Mermaid script
    if "generated_mermaid_script" not in st.session_state:
        st.session_state["generated_mermaid_script"] = ""

    with button1:
        st.markdown("### Generate Mermaid Graph")
        if st.button("🔄 Generate Mermaid Graph", use_container_width=True):
            nx_graph = context["detailed_nx_graph"]
            mermaid_script = get_mermaid_scripts(nx_graph)
            st.session_state["generated_mermaid_script"] = mermaid_script
            st.success("✅ Mermaid graph generated!")

    with header:
        st.markdown("### Mermaid Graph:")

    with mermaid_graph:
        if st.session_state["generated_mermaid_script"]:
            render_mermaid_graph(st.session_state["generated_mermaid_script"])
        else:
            st.info("⚡ Please generate the Mermaid graph first.")

    with script_box:
        if st.session_state["generated_mermaid_script"]:
            st.markdown("### 📜 Mermaid Script:")
            st.markdown("(`Ctrl+A` to select all, `Ctrl+C` to copy.):")
            st.text_area(
                "Mermaid Code",
                value=st.session_state["generated_mermaid_script"],
                height=300,
                key="mermaid_script_textarea",
            )
