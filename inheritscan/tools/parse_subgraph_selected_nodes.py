from pathlib import Path
import json
import inheritscan

package_root = Path(inheritscan.__file__).parent
runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"


def get_mod_class_method_list(runtime_data_folder):
    # TODO #3: use information from "selected_nodes_subgraph.json",
    # find all methods for each class, and construct the list of class_name, mod, method
    # dictionary with the format shown in the mock.

    # fpath = runtime_data_folder / "selected_nodes_subgraph.json"
    # with open(fpath, 'r') as f:
    #     info = json.load(f)

    mock = [{
        "class_name": "DockerRuntime",
        "mod": "runtime.impl.docker.docker_runtime",
        "method": "m1"
    },
    {
        "class_name": "ModalRuntime",
        "mod": "runtime.impl.modal.modal_runtime",
        "method": "m2"
    },
    {
        "class_name": "RunloopRuntime",
        "mod": "runtime.impl.runloop.runloop_runtime",
        "method": "m3"
    }
    ]
    return mock
