import streamlit as st
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from inheritscan.tools.global_graph import render_global_graph_panel
import threading
import json
import os

selected_nodes = []
flask_app = Flask(__name__)
CORS(flask_app)  # 💥 允许任何来源访问

# clear runtime data
import shutil
import os

runtime_dir = "./.run_time"
if os.path.exists(runtime_dir):
    shutil.rmtree(runtime_dir)
    print(f"🗑️ Deleted: {runtime_dir}")
else:
    print(f"⚠️ Path does not exist: {runtime_dir}")


st.set_page_config(page_title="Class Hierarchy Explorer", layout="wide")
if "flask_started" not in st.session_state:

    @flask_app.route("/receive_selection", methods=["POST"])
    def receive_selection():
        nodes = request.json.get("nodes", [])
        new_entry = nodes[0]
        path = ".run_time/selected_nodes.json"

        os.makedirs(".run_time", exist_ok=True)

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
        try:
            with open(".run_time/selected_nodes.json", "r") as f:
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
    
# -------------------------------------
# Mock Data
# -------------------------------------
mock_clusters = {
    "cluster_core": [f"Class{i}" for i in range(1, 6)],
    "cluster_vision": [f"Class{i}" for i in range(6, 11)],
    "cluster_nlp": [f"Class{i}" for i in range(11, 16)],
}

mock_methods = [f"method_{i}()" for i in range(1, 6)]


def render_subgraph_panel(context: dict) -> dict:
    st.markdown("### 📎 Subgraph View")

    cluster = context.get("selected_cluster")
    if not cluster:
        st.info("No cluster selected. Please choose one in the global graph.")
        return {}

    class_list = mock_clusters.get(cluster, [])
    st.markdown(f"Classes in `{cluster}`:")

    current = context.get("selected_classes", [])
    selected = st.multiselect(
        "Select classes to view in detail:", class_list, default=current
    )

    if selected != current:
        return {"selected_classes": selected}
    return {}


def render_detail_llm_panel(context: dict) -> dict:
    st.markdown("### 🔍 Detailed Class View + LLM")

    selected_classes = context.get("selected_classes", [])
    if not selected_classes:
        st.info("No class selected. Please pick one in subgraph.")
        return {}

    selected_class = selected_classes[0]
    st.markdown(f"**Class:** `{selected_class}`")

    for method in mock_methods:
        st.markdown(f"- `{method}`")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.code(f"def {method}:\n    pass", language="python")
        with col2:
            st.button(f"Simplify {method}", key=f"{selected_class}-{method}")

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
    result = render_subgraph_panel(context)
    if result:
        st.session_state.update(result)

# --- Bottom full-width panel: detail + LLM ---
st.divider()
result = render_detail_llm_panel(context)
if result:
    st.session_state.update(result)
