from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import inheritscan
from pathlib import Path


flask_app = Flask(__name__)
CORS(flask_app)
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