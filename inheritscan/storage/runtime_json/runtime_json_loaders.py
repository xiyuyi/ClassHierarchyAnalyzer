from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import json
from pathlib import Path

import inheritscan


def load_selected_nodes_on_global_graph():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "selected_nodes.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        log.info("📤 [Flask] Returning selected nodes:", data)
    except Exception as e:
        log.info("❌ Error loading selected nodes:", e)
        data = []

    return data


def load_selected_nodes_on_subgraph():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "selected_nodes_subgraph.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        log.info("📤 [Flask] Returning selected nodes on subgraph:", data)
    except Exception as e:
        log.info("❌ Error loading selected nodes on subgraph:", e)
        data = []

    return data


def load_global_inheritance_graph():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "global_class_inheritance_graph.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        log.info("loaded global_class_inheritance_grap.")
    except Exception:
        data = []

    return data


def load_metadata():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "meta.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        log.info("loaded meta data for the session.")
    except Exception:
        data = {}

    return data
