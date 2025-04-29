from abc import ABC
from pathlib import Path
from flask import jsonify
import inheritscan
import json


def load_selected_nodes_on_global_graph():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "selected_nodes.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        print("📤 [Flask] Returning selected nodes:", data)
    except Exception as e:
        print("❌ Error loading selected nodes:", e)
        data = []

    return data


def load_selected_nodes_on_subgraph():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "selected_nodes_subgraph.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        print("📤 [Flask] Returning selected nodes on subgraph:", data)
    except Exception as e:
        print("❌ Error loading selected nodes on subgraph:", e)
        data = []

    return data


def load_global_inheritance_graph():
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "global_class_inheritance_graph.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
        print("loaded global_class_inheritance_grap.")
    except Exception as e:
        data = []

    return data

