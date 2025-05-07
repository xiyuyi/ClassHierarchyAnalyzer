from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import networkx as nx

from inheritscan.tools.ai_summaries import get_summary_manager
from inheritscan.tools.uml_panel.formats import format_class_label


def build_detailed_uml_nx_graph(G: nx.DiGraph) -> nx.DiGraph:
    metadata = load_metadata()
    root_dir = metadata["sumarry_root"]
    code_base_dir = metadata["package_path"]

    sm = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
    )

    uml_g = nx.DiGraph()
    if G:
        for mod, class_name in G.nodes:
            method_names = sm.load_class_methods(
                module_path=mod, class_name=class_name
            )
            class_summary = sm.load_class_summary(
                module_path=mod, class_name=class_name
            )
            if len(method_names) == 0:
                method_names = [""]

            l = format_class_label(class_name, method_names)
            uml_g.add_node(
                class_name,
                label=l,
                full_mod=mod + "." + class_name,
                class_summary=class_summary,
            )

        for edge in G.edges:
            uml_g.add_edge(edge[0][1], edge[1][1])

    return uml_g
