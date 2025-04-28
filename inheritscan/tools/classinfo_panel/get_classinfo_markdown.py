
import inheritscan
from pathlib import Path
import json

from inheritscan.tools.ai_summaries import get_summary_manager

def get_detailed_class_description(context):
    # load the selected class on the detailed class uml diagram, from json.
    # json file path: .run_time/clicked_node_on_detailed_uml.json 
    # us summary manager to retrieve information from archive.
    # aggregate into proper markdown
    # TODO here all FQN should be updated in the future.
    runtime_data_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
    fpath = runtime_data_folder / "clicked_node_on_detailed_uml.json"
    with open(fpath, 'r') as f:
        class_selected = json.load(f)[0]
    mod = class_selected['full_mod'].rsplit('.', 1)[0]
    class_name = class_selected['id']
    
    # TODO use the summary manager to retrive information from the archive
    # should enable UI parameter setting.
    # may retrive information from .env, or something else. design later.
    k={
    "code_base_dir": "/Users/xiyuyi/github_repos/OpenHands/openhands",
    "root_dir": "/Users/xiyuyi/github_repos/ClassHierarchyAnalyzer/sumarry_root",  
    "chain_name": "mock_chain",
    }
    sm = get_summary_manager(**k)
    
    method_names = sm.load_class_methods(module_path=mod, class_name=class_name)
    class_summary = sm.load_class_summary(module_path=mod, class_name=class_name)
    method_str_chunk = ""
    for method_name in method_names:
        method_summary = sm.load_method_summary(
            module_path=mod, class_name=class_name, method_name=method_name)
        
        method_str_chunk += f""""
    - `{method_name}()` — *({method_summary})*
    """


    print(f"class summary: {class_summary}")

    return f"""
    
    #### Class: `{class_name}`

    **Fully Qualified Name (FQN):** `{mod}`

    ---

    #### 📄 Description:
    > {class_summary}

    ---

    #### 🛠️ Major Methods:{method_str_chunk}


"""