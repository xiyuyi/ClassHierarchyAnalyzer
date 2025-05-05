from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import json
import os
import shutil
from pathlib import Path

import inheritscan
from inheritscan.storage.runtime_json.runtime_json_dumpers import dump_metadata
from inheritscan.storage.runtime_json.runtime_json_loaders import load_metadata

runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
root_dir = Path(inheritscan.__file__).parent.parent / "sumarry_root"


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
        ps.append(runtime_folder / "global_class_inheritance_graph.json")
        for p in ps:
            if not os.path.exists(p):
                with open(p, "w") as f:
                    json.dump([], f, indent=2)

        ds = []
        ds.append(runtime_folder / "meta.json")
        for p in ds:
            if not os.path.exists(p):
                with open(p, "w") as f:
                    json.dump({}, f, indent=2)

        print(f"📁 Recreated runtime folder at: {runtime_folder}")
        streamlit.session_state["runtime_initialized"] = True

        # configure initial meta data values
        metadata = load_metadata()

        if "package_name" not in metadata:
            metadata["package_name"] = "openhands"

        if "package_path" not in metadata:
            metadata["package_path"] = (
                "/Users/xiyuyi/github_repos/OpenHands/openhands"
            )

        if "module_cluster_levels" not in metadata:
            metadata["module_cluster_levels"] = 1

        if "runtime_folder" not in metadata:
            metadata["runtime_folder"] = str(runtime_folder)

        if "sumarry_root" not in metadata:
            metadata["sumarry_root"] = str(root_dir)

        if "mock_mode" not in metadata:
            metadata["mock_mode"] = True

        if "chain_name" not in metadata:
            metadata["chain_name"] = "mock_chain"

        if "chunk_summary_chain_name" not in metadata:
            metadata["chunk_summary_chain_name"] = "mock_chain"

        if "method_summary_chain_name" not in metadata:
            metadata["method_summary_chain_name"] = "mock_chain"

        if "class_summary_chain_name" not in metadata:
            metadata["class_summary_chain_name"] = "mock_chain"

        dump_metadata(metadata)
