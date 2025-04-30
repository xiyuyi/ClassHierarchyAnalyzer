from collections import defaultdict
from typing import List, Tuple

from inheritscan.agents.microchains.chains.methods2class import \
    get_methods2class_chain
from inheritscan.core.datatypes import ClassInfo
from inheritscan.storage.summary_mng import SummaryManager


class ClassSummary:
    def __init__(
        self,
        summary_manager: SummaryManager,
        tasks: List[Tuple[str, str, str]],
    ):
        """
        tasks: [(mod, class_name, method name)]
        """
        self.summary_manager = summary_manager
        self.tasks = tasks
        self.aggregated_tasks = defaultdict(list)
        self.aggregated_class_methods_summaries = defaultdict(str)
        # self.aggregated_class_methods_summaries[
        #                     (mod, class_name)
        #                 ] = aggregated_summary

        self.aggregated_class_summaries = defaultdict(dict)
        # self.aggregated_classinfo_queue = []
        self.class_summary_chain_name = summary_manager.summary_chain_name
        self.class_summary_chain = get_methods2class_chain(
            self.class_summary_chain_name
        )
        self._aggretate_tasks()
        self._aggretate_classes()
        self.invoke_queue = [
            k for k in self.aggregated_class_methods_summaries
        ]

    def _aggretate_tasks(self):
        "aggregate list of tasks into {(mod, class_name): " "}"
        for mod, class_name, _ in self.tasks:
            self.aggregated_tasks[(mod, class_name)] = []

    def _aggretate_classes(self):
        "aggregate list of tasks into {(mod, class_name): aggregated_class_methods_summaries}"
        for mod, class_name in self.aggregated_tasks:
            class_info = self.summary_manager.load_classinfo(mod, class_name)

            # Aggregate the summaries for all the method information within this class.
            method_names = class_info.methods.keys()
            aggregated_summary = ""
            for method_name in method_names:
                method_info = class_info.methods[method_name]
                summary = method_info.summary
                aggregated_summary += f"\n\n## Method Name:  {method_name}"
                aggregated_summary += "\n"
                aggregated_summary += summary

            self.aggregated_class_methods_summaries[(mod, class_name)] = (
                aggregated_summary
            )

    def summarize_all_classes(self):
        while self.invoke_queue:
            self._summarize_1_class()

        self.aggregated_classinfo_queue = list(
            self.aggregated_class_summaries.keys()
        )

    def _summarize_1_class(self):
        mod, class_name = self.invoke_queue.pop()
        aggregated_summary = self.aggregated_class_methods_summaries[
            (mod, class_name)
        ]
        summary = self.class_summary_chain.invoke(aggregated_summary)
        self.aggregated_class_summaries[(mod, class_name)] = summary[
            "class_summary"
        ]

    def update_all_classinfo(self):
        while self.aggregated_classinfo_queue:
            self._update_1_classinfo()

    def _update_1_classinfo(self):
        """
        Get one (mod, class name) info, then update the corresponding classinfo to file
        Only pay attention to the "summary" field for MethodInfo objects.
        """

        mod, class_name = self.aggregated_classinfo_queue.pop()

        # get old class_info
        class_info: ClassInfo = self.summary_manager.load_classinfo(
            module_path=mod, class_name=class_name
        )

        class_summary = self.aggregated_class_summaries[(mod, class_name)]
        class_info = self.summary_manager.update_class_summary(
            class_info, class_summary
        )
        # save out.
        self.summary_manager.save_classinfo(class_info)
