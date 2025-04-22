from collections import defaultdict
import copy
import os
from typing import List, Tuple

from inheritscan.agents.microchains.chains.sumarize_chunk import get_chunk_summary_chain
from inheritscan.core.datatypes import ClassInfo, MethodInfo, SnippetInfo
from inheritscan.storage.summary_mng import SummaryManager
from inheritscan.tools.class_code_parse import (
    extract_class_code,
    extract_methods_from_class_code,
)
from inheritscan.tools.method_code_chunker import chunk_method_code


class ChunkSummary:
    # given a list of (modules, classes, method):
    # generate the summaries for them using a minichain.
    # update the summarries in chunk at the class level.
    # organize the result data with defined datatypes and save in designation place.

    def __init__(
        self, summary_manager: SummaryManager, tasks: List[Tuple[str, str, str]]
    ):
        """
        tasks: [(mod, class_name, method name)]
        """
        self.summary_manager = summary_manager
        self.tasks = tasks
        self.aggregated_tasks = defaultdict(list)
        self.aggregated_classes_code = defaultdict(str)
        self.aggregated_methods_code = defaultdict(str)
        self.aggregated_summaries = defaultdict(dict)
        self.aggregated_classinfo_queue = []
        self.snippet_summary_chain_name = summary_manager.summary_chain_name
        self.snippet_summary_chain = get_chunk_summary_chain(
            self.snippet_summary_chain_name
        )
        self._aggretate_tasks()
        self._aggretate_methods()
        self.invoke_queue = [k for k in self.aggregated_methods_code]

    def _aggretate_tasks(self):
        "aggregate list of tasks into {(mod, class_name): list of methods}"
        for mod, class_name, method_name in self.tasks:
            self.aggregated_tasks[(mod, class_name)].append(method_name)

    def _aggretate_methods(self):
        "aggregate list of tasks into {(mod, class_name, method): code}"
        code_base_dir = self.summary_manager.code_base_dir
        for mod, class_name in self.aggregated_tasks:
            # get class code.
            method_names = self.aggregated_tasks[mod, class_name]
            mod_list = mod.split(".")
            mod_list[-1] += ".py"
            file_path = os.path.join(code_base_dir, *mod_list)
            class_code = extract_class_code(file_path, class_name)
            self.aggregated_classes_code[(mod, class_name)] = class_code

            # parse class code into method code
            methods_name2code_map = extract_methods_from_class_code(class_code)

            # assign method codes
            for method_name in method_names:
                self.aggregated_methods_code[(mod, class_name, method_name)] = (
                    methods_name2code_map[method_name]
                )

            # prepare placeholders for the aggregated summaires for each method ( every method)
            self.aggregated_summaries[(mod, class_name)] = {
                method_name: None for method_name in method_names
            }

    def summarize_chunks_for_all_methods(self):
        while self.invoke_queue:
            self.summarize_chunk_for_1_method()

        self.aggregated_classinfo_queue = list(self.aggregated_summaries.keys())

    def summarize_chunk_for_1_method(self):
        mod, class_name, method = self.invoke_queue.pop()
        method_code = self.aggregated_methods_code[(mod, class_name, method)]
        snippets = chunk_method_code(method_code)
        snippets_map = defaultdict(list)
        for i, code_snippet in enumerate(snippets):
            summary = self.snippet_summary_chain.invoke(code_snippet)
            snippets_map[f"chunk_{i}"] = [code_snippet, summary["chunk_summary"]]

        # append to aggregated_summaries
        self.aggregated_summaries[(mod, class_name)][method] = snippets_map

    def update_all_classinfo(self):
        while self.aggregated_classinfo_queue:
            self.update_1_classinfo()

    def update_1_classinfo(self):
        """Get one (mod, class name) info, then update the corresponding classinfo to file"""
        mod, class_name = self.aggregated_classinfo_queue.pop()
        class_code = self.aggregated_classes_code[(mod, class_name)]

        # get class_info
        class_info: ClassInfo = self.summary_manager.load_classinfo(
            module_path=mod, class_name=class_name
        )
        class_info_old = copy.deepcopy(class_info)
        class_info.code = class_code

        # update the data fields in class_info
        method_summaries = self.aggregated_summaries[(mod, class_name)]

        for method_name in method_summaries:
            method_code = self.aggregated_methods_code[(mod, class_name, method_name)]
            snippets_map = method_summaries[method_name]

            method_id = ".".join([mod, class_name, method_name])
            method_kwargs = {
                "id": method_id,
                "code": method_code,
                "module_path": mod,
                "class_name": class_name,
                "method_name": method_name,
            }

            method_info = MethodInfo(**method_kwargs)

            for snippet_name in snippets_map:
                snippet_code = snippets_map[snippet_name][0]
                snippet_summary = snippets_map[snippet_name][1]
                snippet_id = ".".join([mod, class_name, method_name, snippet_name])

                snippet_kwargs = {
                    "id": snippet_id,
                    "code": snippet_code,
                    "summary": snippet_summary,
                    "module_path": mod,
                    "class_name": class_name,
                    "method_name": method_name,
                    "snippet_name": snippet_name,
                    "chain_name": self.snippet_summary_chain_name,
                }

            snippet_info = SnippetInfo(**snippet_kwargs)
            method_info.add_snippet_info(snippet_info)

            class_info.add_method_info(method_info)

        updated_class_info = self.summary_manager.update_classinfo(
            class_info_old, class_info
        )
        self.summary_manager.save_classinfo(updated_class_info)
