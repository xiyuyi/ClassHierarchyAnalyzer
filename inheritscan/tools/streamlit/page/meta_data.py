# inheritscan/tools/ui_blocks/metadata_editor.py

import streamlit as st

from inheritscan.storage.runtime_json.runtime_json_dumpers import dump_metadata
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata


def render_metadata_editor():
    """
    Renders a metadata editing form in the main page.
    - Returns the metadata dict currently shown in the UI (not only after saving).
    - If user clicks "Save", it dumps the metadata, clears cache, and reruns the app.
    """
    st.markdown("### Choose package name and codebase path.")

    # Load existing metadata

    metadata = load_metadata()

    # Render fields
    package_name = st.text_input(
        "### Package name", value=metadata["package_name"]
    )
    package_path = st.text_input(
        "### Codebase path", value=metadata["package_path"]
    )

    module_cluster_levels = st.number_input(
        "Module cluster levels",
        min_value=1,
        max_value=5,
        step=1,
        value=metadata["module_cluster_levels"],
    )

    # Assemble result
    metadata = {
        "package_name": package_name,
        "package_path": package_path,
        "module_cluster_levels": module_cluster_levels,
    }

    # Save button
    if st.button("🛠️ Build Graph"):
        dump_metadata(metadata)
        st.cache_resource.clear()
        st.rerun()

    return metadata
