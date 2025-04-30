import json
from pathlib import Path

from pyvis.network import Network

import inheritscan

package_root = Path(inheritscan.__file__).parent


def build_class_hierarchy_pyvis_network(nx_graph=None, panel=None):
    pyvis_g = Network(
        height="600px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black",
        directed=True,
    )
    for node in nx_graph.nodes(data=True):
        full_mod = node[0][0] + "." + node[0][1]
        # mod = node[1].get("class_name", "EMPTY")
        pyvis_g.add_node(node[0][1], title=full_mod)

    for edge in nx_graph.edges():
        pyvis_g.add_edge(edge[0][1], edge[1][1], arrows="to")

    if panel == "global_graph":
        pyvis_config_path = package_root / "configs" / "globalgraph_pyvis.txt"
    elif panel == "sub_graph":
        pyvis_config_path = package_root / "configs" / "subgraph_pyvis.txt"

    with open(pyvis_config_path, "r") as f:
        config_json_str = json.dumps(
            json.load(f)
        )  # Pyvis needs str，not dict. json.dumps() converts a dict into tr.
    pyvis_g.set_options(config_json_str)

    return pyvis_g
