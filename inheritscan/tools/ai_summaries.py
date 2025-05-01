from typing import List

from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.storage.summary_mng import SummaryManager
from inheritscan.tools.chunk_summary_generation_manager import ChunkSummary
from inheritscan.tools.class_summary_generation_manager import ClassSummary
from inheritscan.tools.method_summary_generation_manager import MethodSummary


def get_ai_summaries(tasks: List[dict]):
    # generate summaries for method chunks
    get_summaries_for_method_chunks(tasks)

    # summarize method summaries from method chunks summaries
    get_summaries_for_method(tasks)

    # get class summaries from method summaries
    get_summaries_for_class(tasks)


def get_summary_manager(
    code_base_dir: str = None, root_dir: str = None, chain_name: str = None
):

    sm = SummaryManager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        summary_chain_name=chain_name,
    )
    return sm


def get_summaries_for_method_chunks(tasks: List[dict]):

    metadata = load_metadata()
    root_dir = metadata["sumarry_root"]
    code_base_dir = metadata["package_path"]
    chain_name = metadata["chunk_summary_chain_name"]

    sm = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        chain_name=chain_name,
    )

    chunk_summary = ChunkSummary(summary_manager=sm, tasks=tasks)
    chunk_summary.get_summaries_for_chunks_for_all_method()
    chunk_summary.update_all_classinfo()
    print("ai summaries at the method chunks level is generated")


def get_summaries_for_method(tasks: List[dict]):

    metadata = load_metadata()
    root_dir = metadata["sumarry_root"]
    code_base_dir = metadata["package_path"]
    chain_name = metadata["method_summary_chain_name"]

    sm = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        chain_name=chain_name,
    )

    method_summary = MethodSummary(summary_manager=sm, tasks=tasks)
    method_summary.get_summaries_for_all_methods_and_classes()
    method_summary.update_all_classinfo()
    print("ai summaries at the method level is generated")


def get_summaries_for_class(tasks: List[dict]):

    metadata = load_metadata()
    root_dir = metadata["sumarry_root"]
    code_base_dir = metadata["package_path"]
    chain_name = metadata["class_summary_chain_name"]

    sm = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        chain_name=chain_name,
    )

    method_summary = ClassSummary(summary_manager=sm, tasks=tasks)
    method_summary.get_summaries_for_all_classes()
    method_summary.update_all_classinfo()
    print("ai summaries at the class level is generated")
