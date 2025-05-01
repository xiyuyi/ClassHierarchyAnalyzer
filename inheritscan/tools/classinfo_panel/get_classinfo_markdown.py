import json
from pathlib import Path

import inheritscan
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata
from inheritscan.tools.ai_summaries import get_summary_manager


def get_detailed_class_description(context):
    # TODO #37 need reformat and clean up
    print("now inside get_detailed_class_description")
    metadata = load_metadata()

    runtime_data_folder = (
        Path(inheritscan.__file__).parent.parent / ".run_time"
    )
    fpath = runtime_data_folder / "clicked_node_on_detailed_uml.json"
    with open(fpath, "r") as f:
        class_selected = json.load(f)[0]

    if len(class_selected) == 0:
        return "No class is selected.\nPlease select a class (click) from the diagram on the left."

    mod = class_selected["full_mod"].rsplit(".", 1)[0]
    class_name = class_selected["id"]
    fqn = metadata["package_name"] + "." + mod + "." + class_name

    metadata = load_metadata()
    root_dir = metadata["sumarry_root"]
    code_base_dir = metadata["package_path"]

    sm_method = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        chain_name=metadata["method_summary_chain_name"],
    )
    sm_class = get_summary_manager(
        root_dir=root_dir,
        code_base_dir=code_base_dir,
        chain_name=metadata["class_summary_chain_name"],
    )

    method_names = sm_class.load_class_methods(
        module_path=mod, class_name=class_name
    )
    class_summary = sm_class.load_class_summary(
        module_path=mod, class_name=class_name
    )

    # construct method_string chunk
    method_str_chunk = ""
    for method_name in method_names:
        method_summary = sm_method.load_method_summary(
            module_path=mod, class_name=class_name, method_name=method_name
        )

        method_str_chunk += f""""
    - `{method_name}()` — *({method_summary})*
    """

    print(f"class summary: {class_summary}")

    result = f"""

    #### Class: `{class_name}`

    **Fully Qualified Name (FQN):** `{fqn}`

    ---

    #### 📄 Description:
    > {class_summary}

    ---

    #### 🛠️ Major Methods:{method_str_chunk}


"""

    return result
