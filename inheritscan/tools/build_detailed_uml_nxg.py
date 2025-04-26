import networkx as nx
from pathlib import Path

from inheritscan.tools.ai_summaries import get_summary_manager

def build_detailed_uml_nx_graph(G: nx.DiGraph, summary_root: Path) -> nx.DiGraph:
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

    sm.load_classinfo()
    
    return None
