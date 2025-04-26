import networkx as nx
from pathlib import Path

from inheritscan.tools.ai_summaries import get_summary_manager
from inheritscan.tools.uml_panel.formats import format_class_label

def build_detailed_uml_nx_graph(G: nx.DiGraph) -> nx.DiGraph:
    # TODO use the summary manager to retrive information from the archive
    # should enable UI parameter setting.
    # may retrive information from .env, or something else. design later.
    k={
    "code_base_dir": "/Users/xiyuyi/github_repos/OpenHands/openhands",
    "root_dir": "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root",  
    "chain_name": "mock_chain",
    }
    sm = get_summary_manager(**k)
    # TODO #7 build the detailed_uml_nx_graph. should look at the mockgraph used in the uml panel module.
    # TODO # current.
    # sm.load_classinfo()
    
    uml_g = nx.DiGraph()
    for mod, class_name in G.nodes:
        method_names = sm.load_class_methods(module_path=mod, class_name=class_name)
        # summary = class_info.summary
        # mod = class_info.module_path
        # method_names = [k for k in class_info.methods]
        if len(method_names) == 0:
            method_names = [""]

        l = format_class_label(class_name, method_names)

        uml_g.add_node(
            class_name,
            label=l,
        )

    for edge in G.edges:
        uml_g.add_edge(edge[0][1], edge[1][1])

    return uml_g
