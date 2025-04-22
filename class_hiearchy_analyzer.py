import streamlit as st
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import json
import os

from inheritscan.tools.global_graph import render_global_graph_panel
from inheritscan.tools.sub_graph import render_sub_graph_panel

selected_nodes = []
flask_app = Flask(__name__)
CORS(flask_app)  # 💥 允许任何来源访问

# clear runtime data
import shutil
import os
from pathlib import Path
import inheritscan

package_root = Path(inheritscan.__file__).parent
runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"

# if os.path.exists(runtime_folder):
#     shutil.rmtree(runtime_folder)
#     print(f"🗑️ Deleted: {runtime_folder}")
# else:
#     print(f"⚠️ Path does not exist: {runtime_folder}")
if "runtime_initialized" not in st.session_state:
    if runtime_folder.exists():
        shutil.rmtree(runtime_folder)
        print(f"🗑️ Deleted runtime folder at: {runtime_folder}")
    runtime_folder.mkdir(exist_ok=True)
    print(f"📁 Recreated runtime folder at: {runtime_folder}")
    st.session_state["runtime_initialized"] = True

st.set_page_config(page_title="Class Hierarchy Explorer", layout="wide")
if "flask_started" not in st.session_state:

    @flask_app.route("/receive_selection", methods=["POST"])
    def receive_selection():
        runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
        path = runtime_folder / "selected_nodes.json"
        nodes = request.json.get("nodes", [])
        new_entry = nodes[0]

        os.makedirs(runtime_folder, exist_ok=True)

        if not os.path.exists(path):
            # First time: create file with one entry in a list
            with open(path, "w") as f:
                json.dump([new_entry], f, indent=2)
        else:
            with open(path, "r") as f:
                try:
                    current_nodes = json.load(f)
                except json.JSONDecodeError:
                    current_nodes = []

            # Build set of (id, full_mod) for fast lookup
            node_set = {(n["id"], n["full_mod"]): n for n in current_nodes}
            key = (new_entry["id"], new_entry["full_mod"])

            # Toggle behavior
            if key in node_set:
                del node_set[key]  # deselect
            else:
                node_set[key] = new_entry  # select

            # Write updated list
            updated_nodes = list(node_set.values())
            with open(path, "w") as f:
                json.dump(updated_nodes, f, indent=2)

        print(f"[Flask] ✅ Toggled in {path}: {new_entry}")
        return {"status": "ok"}

    @flask_app.route("/receive_selection_subgraph", methods=["POST"])
    def receive_selection_subgraph():
        runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
        path = runtime_folder / "selected_nodes_subgraph.json"
        nodes = request.json.get("nodes", [])
        new_entry = nodes[0]

        os.makedirs(runtime_folder, exist_ok=True)

        if not os.path.exists(path):
            # First time: create file with one entry in a list
            with open(path, "w") as f:
                json.dump([new_entry], f, indent=2)
        else:
            with open(path, "r") as f:
                try:
                    current_nodes = json.load(f)
                except json.JSONDecodeError:
                    current_nodes = []

            # Build set of (id, full_mod) for fast lookup
            node_set = {(n["id"], n["full_mod"]): n for n in current_nodes}
            key = (new_entry["id"], new_entry["full_mod"])

            # Toggle behavior
            if key in node_set:
                del node_set[key]  # deselect
            else:
                node_set[key] = new_entry  # select

            # Write updated list
            updated_nodes = list(node_set.values())
            with open(path, "w") as f:
                json.dump(updated_nodes, f, indent=2)

        print(f"[Flask] ✅ Toggled in {path}: {new_entry}")
        return {"status": "ok"}
    
    @flask_app.route("/selected_nodes.json", methods=["GET"])
    def get_selected_nodes():
        runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
        path = runtime_folder / "selected_nodes.json"
        try:
            with open(path, "r") as f:
                data = json.load(f)
            print("📤 [Flask] Returning selected nodes:", data)
        except Exception as e:
            print("❌ Error loading selected nodes:", e)
            data = []
        return jsonify(data)
    
    @flask_app.route("/selected_nodes_subgraph.json", methods=["GET"])
    def get_selected_nodes_subgraph():
        runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
        path = runtime_folder / "selected_nodes_subgraph.json"
        try:
            with open(path, "r") as f:
                data = json.load(f)
            print("📤 [Flask] Returning selected nodes:", data)
        except Exception as e:
            print("❌ Error loading selected nodes:", e)
            data = []
        return jsonify(data)

    def run_flask():
        flask_app.run(port=5555, host="127.0.0.1")

    threading.Thread(target=run_flask, daemon=True).start()
    st.session_state["flask_started"] = True
    print("🚀 Flask service started.")

# -------------------------------------
# Initial State
# -------------------------------------
if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = None

if "selected_classes" not in st.session_state:
    st.session_state.selected_classes = []

if "selected_class_detail" not in st.session_state:
    st.session_state.selected_class_detail = None

if "class_hierachy_network_graph" not in st.session_state:
    st.session_state.class_hierachy_network_graph = None



def render_detail_llm_panel(context: dict) -> dict:
    st.markdown("### 🔍 Detailed Class View")

    selected_classes = context.get("selected_classes", [])
    if not selected_classes:
        st.info("No class selected. Please pick one in subgraph.")
        return {}

    selected_class = selected_classes[0]
    st.markdown(f"**Class:** `{selected_class}`")

    if selected_class != context.get("selected_class_detail"):
        return {"selected_class_detail": selected_class}
    return {}


# -------------------------------------
# Page Layout
# -------------------------------------
st.title("📘 Class Hierarchy Explorer")
st.markdown("Visualize and analyze class relationships across modules.")

# Build context from session_state
context = {
    "class_hierachy_network_graph": st.session_state.class_hierachy_network_graph,
    "selected_cluster": st.session_state.selected_cluster,
    "selected_classes": st.session_state.selected_classes,
    "selected_class_detail": st.session_state.selected_class_detail,
}

# --- Top panels: global + subgraph ---
print("render")
top_left, top_right = st.columns(2)


with top_left:
    result = render_global_graph_panel(context)
    if result:
        st.session_state.update(result)

with top_right:
    st.markdown("### 📎 Subgraph View")

    # ✅ Button always stays fixed
    if st.button("🔁 Render Subgraph", use_container_width=True):
        st.session_state["rerender_subgraph"] = True

    # ✅ Render area isolated from button
    subgraph_container = st.container()
    with subgraph_container:
        if st.session_state.get("rerender_subgraph", True):
            result = render_sub_graph_panel(context)
            if result:
                st.session_state.update(result)



# --- Bottom full-width panel: detail + LLM ---
st.divider()
result = render_detail_llm_panel(context)
if result:
    st.session_state.update(result)
