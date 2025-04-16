import streamlit as st
import random

from inheritscan.tools.global_graph import render_global_graph_panel

st.set_page_config(page_title="Class Hierarchy Explorer", layout="wide")

# -------------------------------------
# Initial State
# -------------------------------------
if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = None

if "selected_classes" not in st.session_state:
    st.session_state.selected_classes = []

if "selected_class_detail" not in st.session_state:
    st.session_state.selected_class_detail = None

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
    selected = st.multiselect("Select classes to view in detail:", class_list, default=current)

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
    "selected_cluster": st.session_state.selected_cluster,
    "selected_classes": st.session_state.selected_classes,
    "selected_class_detail": st.session_state.selected_class_detail,
}

# --- Top panels: global + subgraph ---
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
