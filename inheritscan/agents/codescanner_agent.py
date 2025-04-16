import os
from typing import Dict, List
from collections import defaultdict

from myagents.utils.import_parser import extract_imports_exports


class CodeScannerAgent:
    def __call__(self, state: dict) -> dict:
        print(state)
        state["started"] = "modified"
        base_path = state["codebase_path"]
        package_name = state["package_name"]
        N = state["module_cluster_levels"]
        state["modules_details"] = {}
        state["modules_name2path"] = {}
        state["modules_path2name"] = {}
        modules = []

        # Recursively traverse all directories and subdirectories
        for root, dirs, files in os.walk(base_path):
            # Skip special directories
            if any(x in root for x in ["__pycache__", ".venv", ".git", "tests"]):
                continue
            # Process all Python files in current directory except __init__.py
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    full_path = os.path.join(root, file)
                    modules.append(full_path)

        # Analyze imports for each module
        modules_name2path = {}
        modules_path2name = {}
        modules_details = {}
        for filepath in modules:
            module_name = self.get_module_name(filepath, base_path)
            internal_imports, internal_import_alias, external_imports, exports = (
                self.extract_imports_exports(filepath, base_path, package_name)
            )
            exports[module_name] = exports
            modules_name2path[module_name] = filepath
            modules_path2name[filepath] = module_name
            module_details = {
                "internal_imports": internal_imports,
                "internal_import_alias": internal_import_alias,
                "external_imports": external_imports,
                "exports": exports,
            }
            modules_details[module_name] = module_details

        # Group modules by package hierarchy up to level N from base_path
        clusters = defaultdict(list)
        for mod in modules_name2path:
            # Get module path relative to base_path
            rel_path = os.path.join(base_path, mod.replace(".", os.sep))
            parts = os.path.relpath(rel_path, base_path).split(os.sep)
            # Create clusters for each level up to N from base_path
            for i in range(min(N, len(parts))):
                pkg_path = os.path.sep.join(parts[: i + 1])
                clusters[pkg_path].append(mod)

        state["clusters"] = clusters
        state["modules_name2path"] = modules_name2path
        state["modules_path2name"] = modules_path2name
        state["modules_details"] = modules_details

        # aggregate all internal classes and functions
        internal_functions = set()
        internal_classes = set()
        for mod in state["modules_name2path"]:
            for c in state["modules_details"][mod]["exports"]["classes"]:
                internal_classes.add((mod, c))
            for f in state["modules_details"][mod]["exports"]["functions"]:
                internal_functions.add((mod, c))

        state["internal_classes"] = internal_classes
        state["internal_functions"] = internal_functions

        state["modules_to_process"] = list(state["modules_path2name"].keys())[::-1]

        return state

    def get_module_name(self, filepath: str, base_path: str) -> str:
        rel_path = os.path.relpath(filepath, base_path)
        no_ext = os.path.splitext(rel_path)[0]
        return no_ext.replace(os.sep, ".")

    def extract_imports_exports(
        self, filepath: str, base_path: str, package_name: str
    ) -> tuple[List[str], List[str]]:
        return extract_imports_exports(filepath, base_path, package_name)
