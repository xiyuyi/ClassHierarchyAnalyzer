from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

# inheritscan/tools/ui_blocks/metadata_editor.py

import streamlit as st

from inheritscan.storage.graph_mng import GraphManager
from inheritscan.storage.runtime_json.runtime_json_dumpers import dump_metadata
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata


def render_metadata_editor():
    """
    Renders a metadata editing form in the main page.
    - Returns the metadata dict currently shown in the UI (not only after saving).
    - If user clicks "Save", it dumps the metadata, clears cache, and reruns the app.
    """
    # Load existing metadata
    metadata = load_metadata()

    st.markdown("#### Set codebase path, packge name below:")

    c1, c2 = st.columns(2)
    with c1:
        package_path = st.text_input(
            "Codebase path (e.g. ~/repo/package_src)",
            value=metadata["package_path"],
        )

    with c2:
        # Render fields
        package_name = st.text_input(
            "Package name (e.g. openhands)", value=metadata["package_name"]
        )

    # st.divider()
    on = st.toggle("Mock mode", True)
    mock_mode = True if on else False
    chain_name = "mock_chain" if on else "qwen_coder_32b_instruct500_engilsh"
    cls_sum_chain = "mock_chain" if on else "qwen_32b_1_paragraph"

    st.divider()

    # Assemble result
    metadata.update(
        {
            "package_name": package_name,
            "package_path": package_path,
            "module_cluster_levels": 1,
            "mock_mode": mock_mode,
            "chain_name": chain_name,
            "chunk_summary_chain_name": chain_name,  # may configure these chains differently in the future.
            "method_summary_chain_name": chain_name,
            "class_summary_chain_name": cls_sum_chain,
        }
    )

    # Save button
    if st.button("🛠️ Build Graph"):
        dump_metadata(metadata)
        nx_graph = st.session_state.class_hierarchy_network_graph
        GraphManager.write_global_graph(nx_graph)

    return metadata
