import ast
import json
import os
from pathlib import Path

import inheritscan


def find_class_def_line(filepath: str, class_name: str) -> int:
    """
    Return the line number where `class_name` is defined in the given file.
    """
    with open(filepath, "r") as f:
        tree = ast.parse(f.read(), filename=filepath)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node.lineno

    raise ValueError(f"Class `{class_name}` not found in {filepath}")


def open_selected_file_in_vscode(contex):
    runtime_data_folder = (
        Path(inheritscan.__file__).parent.parent / ".run_time"
    )
    fpath = runtime_data_folder / "clicked_node_on_detailed_uml.json"
    with open(fpath, "r") as f:
        class_selected = json.load(f)[0]

    if len(class_selected) == 0:
        return "No class is selected.\nPlease select a class (click) from the diagram on the left."

    mod = class_selected["full_mod"].rsplit(".", 1)[0].split(".")
    print("debug in open_selected_file_in_vscode")
    print("mod")
    print(mod)

    class_name = class_selected["id"]

    code_base_dir = "/Users/xiyuyi/github_repos/OpenHands/openhands"
    py_path = Path(code_base_dir, *mod[:-1], mod[-1] + ".py")
    print("package_path")
    print(code_base_dir)
    print("py_path")
    print(py_path)
    lineno = find_class_def_line(py_path, class_name)
    os.system(f"code -g {py_path}:{lineno}")
