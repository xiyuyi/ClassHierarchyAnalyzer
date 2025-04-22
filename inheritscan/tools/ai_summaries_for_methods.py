from typing import List

from inheritscan.storage.summary_mng import SummaryManager
from inheritscan.tools.chunk_summary_generation_manager import ChunkSummary


def generate_ai_summaries_for_method(tasks: List[dict]):
    # TODO #3: generate ai summaries for the given collection of methods.
    
    # generate summaries for method chunks
    get_summaries_for_method_chunks(tasks)

    # summarize method summaries from method chunks summary
    get_summarize_chunk_sums_for_method(tasks)
    pass


def get_summaries_for_method_chunks(tasks: List[dict]):
    # TODO #4: relevant to issue $4, expose path selection #4
    # expose code_base)dir, root_dir to context. 
    # add button for selection.
    # code_base_dir is also used in global_graph.py
    # consider context['project_info']
    code_base_dir = "/Users/xiyuyi/github_repos/OpenHands/openhands"
    root_dir = "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root"
    chain_name = "mock_chain"

    sm = SummaryManager(root_dir = root_dir, 
                    code_base_dir = code_base_dir,
                    summary_chain_name = chain_name)
    cs = ChunkSummary(summary_manager=sm, tasks = tasks)
    cs.summarize_chunks_for_all_methods()
    cs.update_all_classinfo()

    print("ai summaries at the method chunks level is generated")


def get_summarize_chunk_sums_for_method(tasks: List[dict]):
    # TODO #5 minichain for summary aggregation to achieve method level summary.
    pass