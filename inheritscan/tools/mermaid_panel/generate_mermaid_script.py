from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

from pathlib import Path

import inheritscan
from inheritscan.storage.summary_mng import SummaryManager
from inheritscan.tools.ai_summaries import get_summary_manager


def _build_method_string_segment(methods):
    res = ""
    for method in methods:
        res += f"        +{method}()\n"
    return res


def _build_class_segment(class_name, methods):
    method_segment = _build_method_string_segment(methods)
    res = f"    class {class_name} {{\n{method_segment}    }}\n"
    return res


def _get_class_table(nx_graph):
    class_table = {}
    for node in nx_graph.nodes:
        # example node:
        # ('runtime.impl.local.local_runtime', 'LocalRuntime')
        node[0] + "." + node[1]
        # set deduplicated class names
        counter, class_key = 1, node[1]
        while class_key in class_table:
            class_key = node[1] + f"[{counter}]"
            counter += 1
        class_table[node] = class_key
    return class_table


def _get_aggregated_class_segments(class_table, sm: SummaryManager):
    aggregated_class_segment = ""

    for node, class_key in class_table.items():
        module_path = node[0]
        class_name = node[1]
        methods = sm.load_class_methods(
            module_path=module_path, class_name=class_name
        )

        # remove hidden methods
        methods = [m for m in methods if (not m.startswith("_"))]
        aggregated_class_segment += "\n" + _build_class_segment(
            class_key, methods
        )

    return aggregated_class_segment


def _aggregate_inheritance_segments(nx_graph, class_table):
    res = ""
    for edge in nx_graph.edges:
        parent = class_table[edge[0]]
        child = class_table[edge[1]]
        inheritance_segment = f"\n    {parent} <|-- {child}"
        res += inheritance_segment

    return res


def get_mermaid_scripts(nx_graph):
    """populate mermaid script in json archive."""
    runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    class_table = _get_class_table(nx_graph)
    log.info("class_table:")
    log.info(class_table)

    metadata = load_metadata()
    root_dir = metadata["sumarry_root"]
    code_base_dir = metadata["package_path"]
    chain_name = metadata["class_summary_chain_name"]

    sm = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        chain_name=chain_name,
    )
    class_block = _get_aggregated_class_segments(class_table, sm)
    inheritance_block = _aggregate_inheritance_segments(nx_graph, class_table)
    script = f"classDiagram\n{class_block}\n{inheritance_block}"

    fpath = runtime_folder / "./detailed_class_view_mermaid.mmd"
    with open(fpath, "w") as f:
        f.write(script)

    return script
