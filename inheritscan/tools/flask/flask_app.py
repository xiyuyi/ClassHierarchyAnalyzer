from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import inheritscan
from pathlib import Path

from inheritscan.storage.runtime_json.runtime_json_dumpers import (
    dump_clicked_node_on_detailed_uml,
    dump_selected_nodes_on_global_graph,
    dump_selected_nodes_on_subgraph,
)
from inheritscan.storage.runtime_json.runtime_json_loaders import (
    load_selected_nodes_on_global_graph,
    load_selected_nodes_on_subgraph,
)

flask_app = Flask(__name__)
CORS(flask_app)


@flask_app.route("/receive_selection", methods=["POST"])
def receive_selection():
    nodes = request.json.get("nodes", [])
    dump_selected_nodes_on_global_graph(nodes)
    return {"status": "ok"}


@flask_app.route("/receive_selection_subgraph", methods=["POST"])
def receive_selection_subgraph():
    nodes = request.json.get("nodes", [])
    dump_selected_nodes_on_subgraph(nodes)
    return {"status": "ok"}


@flask_app.route("/receive_the_clicked_node_detailed_uml", methods=["POST"])
def receive_seleced_class():
    nodes = request.json.get("nodes", [])
    dump_clicked_node_on_detailed_uml(nodes)
    return {"status": "ok"}


@flask_app.route("/selected_nodes.json", methods=["GET"])
def get_selected_nodes():
    data = load_selected_nodes_on_global_graph()
    return jsonify(data)


@flask_app.route("/selected_nodes_subgraph.json", methods=["GET"])
def get_selected_nodes_subgraph():
    data = load_selected_nodes_on_subgraph()
    return jsonify(data)


def run_flask():
    flask_app.run(port=5555, host="127.0.0.1")
