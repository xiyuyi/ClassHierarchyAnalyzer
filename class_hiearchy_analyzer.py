import threading
from pathlib import Path

import streamlit as st

import inheritscan
from inheritscan.storage.runtime_json.runtime_json_dumpers import dump_metadata
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.flask.flask_app import run_flask
from inheritscan.tools.mermaid_panel.entry import render_mermaid_panel
from inheritscan.tools.streamlit.init_json_files import initialize_json_files
from inheritscan.tools.streamlit.init_state import initialize_session_state
from inheritscan.tools.streamlit.page.bottom_left import render_bottom_left
from inheritscan.tools.streamlit.page.bottom_right import render_bottom_right
from inheritscan.tools.streamlit.page.meta_data import render_metadata_editor
from inheritscan.tools.streamlit.page.top_left import render_top_left
from inheritscan.tools.streamlit.page.top_right import render_top_right

package_root = Path(inheritscan.__file__).parent
runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
root_dir = Path(inheritscan.__file__).parent.parent / "sumarry_root"

# Initialize session state
initialize_session_state(st)

# Initialize json files in runtime_folder:
initialize_json_files(streamlit=st, runtime_folder=runtime_folder)

# put place holder json. files
metadata = load_metadata()
dump_metadata(metadata)


# Start flask:
if "flask_started" not in st.session_state:
    threading.Thread(target=run_flask, daemon=True).start()
    st.session_state["flask_started"] = True
    print("🚀 Flask service started.")

# Page Layout
st.set_page_config(page_title="Class Inheritance Explorer", layout="wide")
st.title("📘 Class Inheritance Explorer")
st.markdown(
    "Explore and analyze class inheritance structures across your Python codebase."
)
metadata_panel = st.container()
top_left, top_right = st.columns(2)
st.divider()
bottom_left, bottom_right = st.columns(2)
st.divider()
mermaid_panel = st.container()

# Prepare Context
context = {
    "class_hierarchy_network_graph": st.session_state.class_hierarchy_network_graph,
    "selected_cluster": st.session_state.selected_cluster,
    "selected_classes": st.session_state.selected_classes,
    "selected_class_detail": st.session_state.selected_class_detail,
    "modules_name2path": st.session_state.modules_name2path,
    "modules_details": st.session_state.modules_details,
    "detailed_uml_class_graph": st.session_state.detailed_uml_class_graph,
    "detailed_nx_graph": st.session_state.detailed_nx_graph,
}

# Render

# call at top of page
with metadata_panel:
    render_metadata_editor()

with top_left:
    render_top_left(context)

with top_right:
    render_top_right(context)

with bottom_left:
    render_bottom_left(context)

with bottom_right:
    render_bottom_right(context)

with mermaid_panel:
    render_mermaid_panel(context)

print("All session_state keys:")
for key in list(st.session_state.keys()):
    print(key)
