from typing import List

from inheritscan.storage.summary_mng import SummaryManager
from inheritscan.tools.chunk_summary_generation_manager import ChunkSummary
from inheritscan.tools.method_summary_generation_manager import MethodSummary
from inheritscan.tools.class_summary_generation_manager import ClassSummary


def generate_ai_summaries(tasks: List[dict]):
    # TODO #3: generate ai summaries for the given collection of methods.
    
    # generate summaries for method chunks
    get_summaries_for_method_chunks(tasks)

    # summarize method summaries from method chunks summaries
    get_summaries_for_method(tasks)

    # get class summaries from method summaries
    get_summaries_for_class(tasks)
    pass



def get_summary_manager(code_base_dir: str = None, root_dir: str = None, chain_name: str = None):
    # TODO #4: relevant to issue $4, expose path selection #4
    # expose code_base)dir, root_dir to context. 
    # add button for selection.
    # code_base_dir is also used in global_graph.py
    # consider context['project_info']
    if not code_base_dir:
        code_base_dir = "/Users/xiyuyi/github_repos/OpenHands/openhands"

    if not root_dir:    
        root_dir = "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root"
    
    if not chain_name:
        # chain_name = "qwen_coder_32b_instruct500_engilsh"
        chain_name = "mock_chain"

    sm = SummaryManager(root_dir = root_dir, 
                    code_base_dir = code_base_dir,
                    summary_chain_name = chain_name)
    return sm


def get_summaries_for_method_chunks(tasks: List[dict]):
    k={
    "code_base_dir": "/Users/xiyuyi/github_repos/OpenHands/openhands",
    "root_dir": "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root",  
    "chain_name": "qwen_coder_32b_instruct500_engilsh"
    # "chain_name": "mock_chain",
    }
    sm = get_summary_manager(**k)
    chunk_summary = ChunkSummary(summary_manager=sm, tasks = tasks)
    chunk_summary.summarize_chunks_for_all_methods()
    chunk_summary.update_all_classinfo()
    print("ai summaries at the method chunks level is generated")



def get_summaries_for_method(tasks: List[dict]):
    # TODO #5 llm minichain: chunk summary -> method summary
    # minichain for summary aggregation to achieve method level summary.
    k={
    "code_base_dir": "/Users/xiyuyi/github_repos/OpenHands/openhands",
    "root_dir": "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root",  
    "chain_name": "qwen_coder_32b_instruct500_engilsh"
    # "chain_name": "mock_chain",
    }
    sm = get_summary_manager(**k)
    method_summary = MethodSummary(summary_manager=sm, tasks = tasks)
    method_summary.summarize_methods_for_all_classes()
    method_summary.update_all_classinfo()
    print("ai summaries at the method level is generated")

def get_summaries_for_class(tasks: List[dict]):
    # TODO #6 minichain for summary aggregation to achieve class level summary.
    k={
    "code_base_dir": "/Users/xiyuyi/github_repos/OpenHands/openhands",
    "root_dir": "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root",  
    "chain_name": "qwen_coder_32b_instruct2000_engilsh"
    # "chain_name": "mock_chain",
    }
    sm = get_summary_manager(**k)
    method_summary = ClassSummary(summary_manager=sm, tasks = tasks)
    method_summary.summarize_all_classes()
    method_summary.update_all_classinfo()
    print("ai summaries at the class level is generated")
