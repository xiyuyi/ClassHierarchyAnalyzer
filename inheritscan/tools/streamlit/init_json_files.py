import os
import json
import shutil
import streamlit


def initialize_json_files(streamlit, json_dir):
    
    if "runtime_initialized" not in streamlit.session_state:
        if json_dir.exists():
            shutil.rmtree(json_dir)
            print(f"🗑️ Deleted runtime folder at: {json_dir}")

        json_dir.mkdir(exist_ok=True)

        ps = []
        ps.append(json_dir / "selected_nodes.json")
        ps.append(json_dir / "selected_nodes_subgraph.json")
        ps.append(json_dir / "clicked_node_on_detailed_uml.json")
        ps.append(json_dir / "detailed_class_view_mermaid.json")
        for p in ps:
            if not os.path.exists(p):
                with open(p, "w") as f:
                    json.dump([], f, indent=2)

        print(f"📁 Recreated runtime folder at: {json_dir}")

        streamlit.session_state["runtime_initialized"] = True
