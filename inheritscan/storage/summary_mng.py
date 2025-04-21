import os
import json

from inheritscan.core.datatypes import ClassInfo


class SummaryManager:
    def __init__(self, root_dir="summaries"):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)

    def get_path(self, module_path: str, class_name: str) -> str:
        subdir = os.path.join(self.root_dir, *module_path.split('.'))
        os.makedirs(subdir, exist_ok=True)
        return os.path.join(subdir, f"{class_name}.json")

    def save_classinfo(self, class_info: ClassInfo):
        path = self.get_path(class_info.module_path, class_info.class_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(class_info.to_dict(), f, indent=2)

    def load_classinfo(self, module_path: str, class_name: str) -> ClassInfo:
        path = self.get_path(module_path, class_name)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return ClassInfo.from_dict(data)
