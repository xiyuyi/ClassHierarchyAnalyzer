from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

from pathlib import Path

import inheritscan
from inheritscan.storage.runtime_json.runtime_json_dumpers import \
    dump_global_inheritance_graph
from inheritscan.storage.runtime_json.runtime_json_loaders import (
    load_global_inheritance_graph, load_metadata)


class GraphManager:
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    meta_fpath = runtime_folder / "meta.json"

    @classmethod
    def write_global_graph(cls, nx_global):
        data = load_metadata()
        package_name = data["package_name"]

        # use FQN as the key for each class.
        class_table = {}
        for node in nx_global.nodes:
            fqn = package_name + "." + ".".join(node)
            class_table[fqn] = []

        for edge in nx_global.edges:
            fqn_parent = package_name + "." + ".".join(edge[1])
            fqn_child = package_name + "." + ".".join(edge[0])
            class_table[fqn_parent].append(fqn_child)

        dump_global_inheritance_graph(class_table)
        # save global graph inforamtion to json archive.

    @classmethod
    def load_global_graph(cls):
        return load_global_inheritance_graph()
