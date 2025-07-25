from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import json
import os

from inheritscan.core.datatypes import ClassInfo, SnippetInfo
from inheritscan.tools.recursive_update_dict import recursive_update


class SummaryManager:
    # root_dir: the root_dir for the summary information aggregation folder
    # code_base_dir is the dir of the codebase root.
    # summary_chain_name: name fo the llmchain for summary generation

    # this class interface with a ClassInfo object.
    # Each ClassInfo object is stored in the format of a .json file under the root_dir with project dir structure
    # this summary manger load the classinfo from .json file.
    # update classinfo1 with information in classinfo2
    # saves ClassInfo object to .json file.
    # load and reconstitute ClassInfo object from .json file.
    # update_classinfo: update classinfo_old with information in classinfo_new

    def __init__(
        self,
        root_dir: str,
        code_base_dir: str,
        summary_chain_name="tinyllama150_korean",
    ):
        self.root_dir = root_dir
        self.code_base_dir = code_base_dir
        self.summary_chain_name = summary_chain_name
        os.makedirs(self.root_dir, exist_ok=True)

    def get_path(self, module_path: str, class_name: str) -> str:
        subdir = os.path.join(self.root_dir, *module_path.split("."))
        os.makedirs(subdir, exist_ok=True)
        return os.path.join(subdir, f"{class_name}.json")

    def save_classinfo(self, class_info: ClassInfo):
        path = self.get_path(class_info.module_path, class_info.class_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(class_info.to_dict(), f, indent=2, ensure_ascii=False)

    def load_classinfo(self, module_path: str, class_name: str) -> ClassInfo:
        """

        Example:
            module_path = "memory.condenser.condenser.Condenser"
            class_name = "Condenser"
            class_info = load_classinfo(module_path, class_name)
        """
        path = self.get_path(module_path, class_name)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return ClassInfo.from_dict(data)
        else:
            class_id = ".".join([module_path, class_name])
            class_kwargs = {
                "id": class_id,
                "code": None,
                "module_path": module_path,
                "class_name": class_name,
            }
            return ClassInfo(**class_kwargs)

    def update_classinfo(self, c0: ClassInfo, c1: ClassInfo):
        """update c0 based on c1's information."""
        d0 = c0.to_dict()
        d1 = c1.to_dict()
        recursive_update(d0, d1)
        return ClassInfo.from_dict(d0)

    def update_methods_summaries(self, c: ClassInfo, method_summaries: dict):
        # update_methods_summaries(self, c: ClassInfo, method_name: str, summary: str):
        """update method summaries of all methods in c"""
        d = c.to_dict()
        for method_name in method_summaries:
            summary = method_summaries[method_name]
            d["methods"][method_name]["summary"] = summary
            d["methods"][method_name]["chain_name"] = self.summary_chain_name

        return ClassInfo.from_dict(d)

    def update_class_summary(self, c: ClassInfo, class_summary: str):
        """update class summary"""
        d = c.to_dict()
        d["summary"] = class_summary
        d["chain_name"] = self.summary_chain_name

        return ClassInfo.from_dict(d)

    def load_class_methods(self, module_path: str, class_name: str):
        class_info = self.load_classinfo(
            module_path=module_path, class_name=class_name
        )
        methods = []
        methods = [k for k in class_info.methods]
        return methods

    def load_class_summary(self, module_path: str, class_name: str):
        class_info = self.load_classinfo(
            module_path=module_path, class_name=class_name
        )

        if class_info.chain_name == self.summary_chain_name:
            return class_info.summary
        else:
            # need to change to logger.
            print(
                f"class_info.chain_name {class_info.chain_name}, self.summary_chain_name {self.summary_chain_name}"
            )

        return None

    def load_method_summary(
        self, module_path: str, class_name: str, method_name: str
    ):
        class_info: ClassInfo = self.load_classinfo(
            module_path=module_path, class_name=class_name
        )
        if method_name in class_info.methods:
            method_info = class_info.methods[method_name]
            if method_info.chain_name == self.summary_chain_name:
                summary = method_info.summary
                return summary
        return None

    def load_snippet_summary(
        self,
        module_path: str,
        class_name: str,
        method_name: str,
        snippet_name: str,
    ):
        class_info: ClassInfo = self.load_classinfo(
            module_path=module_path, class_name=class_name
        )
        chain_name = None
        if method_name in class_info.methods:
            method_info = class_info.methods[method_name]
            if snippet_name in method_info.snippets:
                snippet_info: SnippetInfo = class_info.methods[
                    method_name
                ].snippets[snippet_name]
                chain_name = snippet_info.chain_name
                if snippet_info.chain_name == self.summary_chain_name:
                    summary = snippet_info.summary
                    if summary is not None:
                        print(
                            f"Sucessfully loaded snippet summary {module_path}, {class_name}, {method_name}, {snippet_name}"
                        )
                        log.info(summary)
                        return summary
                    else:
                        pass
                else:
                    log.info("chain mismatch")
                    print(
                        f"snippet_info.chain_name: {snippet_info.chain_name}, and self.summary_chain_name: {self.summary_chain_name}"
                    )
            else:
                print(
                    f"snippet_name {snippet_name} not found in method_info.snippets"
                )
        else:
            log.info(
                f"method_name {method_name} not found in class_info.methods"
            )

        summary = None
        print(
            f"Didn't find snippet summary {module_path}, {class_name}, {method_name}, {snippet_name}"
        )

        if chain_name:
            print(
                f"found summary {summary} for chain [{chain_name}], will update this field."
            )

        return None
