# inheritscan/tools/ui_blocks/metadata_editor.py

import streamlit as st

from inheritscan.storage.runtime_json.runtime_json_dumpers import dump_metadata
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata


def render_metadata_editor(defaults: dict = None) -> dict:
    """
    Renders a metadata editing form in the main page.
    - Returns the metadata dict currently shown in the UI (not only after saving).
    - If user clicks "Save", it dumps the metadata, clears cache, and reruns the app.
    """
    st.markdown("### 🛠️ Configure Class Graph Metadata")

    # Load existing metadata
    try:
        existing_metadata = load_metadata()
    except:
        existing_metadata = {}

    # Default values
    default_metadata = {
        "package_name": "openhands",
        "package_path": "/Users/xiyuyi/github_repos/OpenHands/openhands",
        "module_cluster_levels": 1,
    }
    if defaults:
        default_metadata.update(defaults)
    default_metadata.update(existing_metadata)

    # Render fields
    package_name = st.text_input(
        "Package name", value=default_metadata["package_name"]
    )
    package_path = st.text_input(
        "Codebase path", value=default_metadata["package_path"]
    )
    module_cluster_levels = st.number_input(
        "Module cluster levels",
        min_value=1,
        max_value=5,
        step=1,
        value=default_metadata["module_cluster_levels"],
    )

    # Assemble result
    metadata = {
        "package_name": package_name,
        "package_path": package_path,
        "module_cluster_levels": module_cluster_levels,
    }

    # Save button
    if st.button("💾 Save Metadata & Rebuild Graph"):
        dump_metadata(metadata)
        st.cache_resource.clear()
        st.rerun()

    return metadata
