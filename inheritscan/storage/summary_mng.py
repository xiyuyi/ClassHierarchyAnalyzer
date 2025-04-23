import os
import json

from inheritscan.core.datatypes import ClassInfo, MethodInfo
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
