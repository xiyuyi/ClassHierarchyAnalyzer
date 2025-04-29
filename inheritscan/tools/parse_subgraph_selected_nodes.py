import json
from pathlib import Path

import inheritscan
from inheritscan.tools.class_code_parse import (
    extract_class_code, extract_methods_from_class_code)

package_root = Path(inheritscan.__file__).parent
runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"


def get_mod_class_method_list(context, mock=False):
    # TODO #3: use information from "selected_nodes_subgraph.json",
    # find all methods for each class, and construct the list of class_name, mod, method
    # dictionary with the format shown in the mock.

    # fpath = runtime_data_folder / "selected_nodes_subgraph.json"
    # with open(fpath, 'r') as f:
    #     info = json.load(f)
    Path(inheritscan.__file__).parent
    runtime_data_folder = (
        Path(inheritscan.__file__).parent.parent / ".run_time"
    )

    fpath = runtime_data_folder / "selected_nodes_subgraph.json"
    with open(fpath, "r") as f:
        classes = json.load(f)

    res = []
    for c in classes:
        class_name = c["id"]
        mod = c["full_mod"].rsplit(".", 1)[0]

        code_path = context["modules_name2path"][mod]
        class_code = extract_class_code(code_path, class_name)
        method_code_map = extract_methods_from_class_code(class_code)
        for method in method_code_map.keys():
            info = {"class_name": class_name, "mod": mod, "method": method}
            res.append(info)

    if mock:
        res = [
            {
                "class_name": "DockerRuntime",
                "mod": "runtime.impl.docker.docker_runtime",
                "method": "m1",
            },
            {
                "class_name": "ModalRuntime",
                "mod": "runtime.impl.modal.modal_runtime",
                "method": "m2",
            },
            {
                "class_name": "RunloopRuntime",
                "mod": "runtime.impl.runloop.runloop_runtime",
                "method": "m3",
            },
        ]

    return res
