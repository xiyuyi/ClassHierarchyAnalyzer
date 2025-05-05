from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import json
import os
from pathlib import Path

import inheritscan


def _dump_nodes_to_json(nodes, path):
    if not os.path.exists(path):
        # First time: create file with one entry in a list
        with open(path, "w") as f:
            json.dump([nodes], f, indent=2)

    else:
        with open(path, "r") as f:
            try:
                current_nodes = json.load(f)
            except json.JSONDecodeError:
                current_nodes = []

        # Build set of (id, full_mod) for fast lookup
        node_set = {(n["id"], n["full_mod"]): n for n in current_nodes}

        # for the given set of nodes, if any of them is not in node_set, add them all to node_set.
        # if all of them are in the node_set, delete them all to node set.
        node_set_flag = "delete"
        for new_entry in nodes:
            key = (new_entry["id"], new_entry["full_mod"])
            if key not in node_set:
                node_set_flag = "add"
                break

        # Toggle behavior
        for new_entry in nodes:
            key = (new_entry["id"], new_entry["full_mod"])
            if node_set_flag == "delete":
                if key in node_set:
                    del node_set[key]  # deselect
            elif node_set_flag == "add":
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


def dump_clicked_node_on_detailed_uml(nodes):
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "clicked_node_on_detailed_uml.json"
    entry = nodes[0]
    with open(path, "w") as f:
        json.dump([entry], f, indent=2)
    print(f"dumped the clicked node on detailed uml panel to: {path}")


def dump_metadata(metadata: dict[str]):
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "meta.json"
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"dumped metadata to: {path}")


def dump_global_inheritance_graph(global_inheritance_graph: dict[str]):
    # global_graph, key is FQN of each class
    # value is their children. all represented with FQN
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    path = runtime_folder / "global_class_inheritance_graph.json"
    with open(path, "w") as f:
        json.dump(global_inheritance_graph, f, indent=2)
    print(f"dumped global_graph to: {path}")
