import os
import json
import shutil
import streamlit


def initialize_json_files(streamlit, runtime_folder):
    
    if "runtime_initialized" not in streamlit.session_state:
        if runtime_folder.exists():
            shutil.rmtree(runtime_folder)
            print(f"🗑️ Deleted runtime folder at: {runtime_folder}")

        runtime_folder.mkdir(exist_ok=True)

        ps = []
        ps.append(runtime_folder / "selected_nodes.json")
        ps.append(runtime_folder / "selected_nodes_subgraph.json")
        ps.append(runtime_folder / "clicked_node_on_detailed_uml.json")
        ps.append(runtime_folder / "detailed_class_view_mermaid.json")
        ps.append(runtime_folder / "meta.json")
        ps.append(runtime_folder / "global_class_inheritance_graph.json")
        for p in ps:
            if not os.path.exists(p):
                with open(p, "w") as f:
                    json.dump([], f, indent=2)

        print(f"📁 Recreated runtime folder at: {runtime_folder}")
        streamlit.session_state["runtime_initialized"] = True
