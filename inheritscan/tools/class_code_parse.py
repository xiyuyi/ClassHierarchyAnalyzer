import ast
from pathlib import Path
from typing import Dict


def extract_class_code(file_path: str, class_name: str) -> str:
    source = Path(file_path).read_text()
    module = ast.parse(source)
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return ast.get_source_segment(source, node)
    raise ValueError(f"Class '{class_name}' not found in '{file_path}'")


import ast


def extract_methods_from_class_code(class_code: str) -> Dict[str, str]:
    method_map = {}
    class_node = ast.parse(class_code).body[
        0
    ]  # we assume it's one class block

    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            method_name = node.name
            method_code = ast.get_source_segment(class_code, node)
            method_map[method_name] = method_code

    return method_map
