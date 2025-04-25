import inheritscan
import os
from pathlib import Path
import json


def _dump_nodes_to_json(nodes, path):
    new_entry = nodes[0]
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


def dump_selected_nodes_on_subgraph(nodes):
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "selected_nodes_subgraph.json"
    _dump_nodes_to_json(nodes, path)
    print(f"dumped selected nodes on sub-graph to: {path}")


def dump_selected_nodes_on_global_graph(nodes):
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "selected_nodes.json"
    _dump_nodes_to_json(nodes, path)
    print(f"dumped selected nodes on global graph to: {path}")
