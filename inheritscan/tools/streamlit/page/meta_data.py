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
    st.divider()

    # Assemble result
    metadata = {
        "package_name": package_name,
        "package_path": package_path,
        "module_cluster_levels": 1,
        "mock_mode": mock_mode,
    }

    # Save button
    if st.button("🛠️ Build Graph"):
        dump_metadata(metadata)
        nx_graph = st.session_state.class_hierarchy_network_graph
        GraphManager.write_global_graph(nx_graph)

    return metadata
