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
        p1 = json_dir / "selected_nodes.json"
        p2 = json_dir / "selected_nodes_subgraph.json"
    
        for p in [p1, p2]:
            if not os.path.exists(p):
                with open(p, "w") as f:
                    json.dump([], f, indent=2)

        print(f"📁 Recreated runtime folder at: {json_dir}")
        streamlit.session_state["runtime_initialized"] = True
