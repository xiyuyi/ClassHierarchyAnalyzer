import ast
import traceback
from myagents.utils.ast import inspect_class_relations


class MCInheritance:
    def __call__(self, state: dict) -> dict:
        """
        This call focuses on all the class definitions within the module,
        and updat ethe inheritance relation of those classes to the state.
        It handles a single module
        """
        while state["modules_to_process"]:
            # parse information for the module:
            module_path = state["modules_to_process"].pop()
            module_name = state["modules_path2name"][module_path]
            internal_import_alias = state["modules_details"][module_name][
                "internal_import_alias"
            ]
            # {realname: (module_name, usedname)}

            # build ast tree for the module:
            try:
                with open(module_path, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source)
            except (SyntaxError, UnicodeDecodeError):
                print(f"[WARN] Failed to parse: {module_path}")
                return state

            # loop over all class definition nodes, and populate the class dependency relation table
            try:
                class_inheritances = {}
                # class_inheritances: {(module name, class name): {"inherits": [(base module, base class name),...]}}
                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        relations = inspect_class_relations(
                            module_name, node, internal_import_alias
                        )
                        class_inheritances.update(relations)
            except:
                print(f"Inheritance analysis failed at {module_path}")
                traceback.print_exc()
                return state

            state["modules_details"][module_name][
                "class_inheritances"
            ] = class_inheritances

        return state
