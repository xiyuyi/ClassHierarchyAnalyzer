def build_graph_state_from_metadata(metadata):
    state = {
        "package_name": metadata["package_name"],
        "codebase_path": metadata["package_path"],
        "module_cluster_levels": metadata["module_cluster_levels"],
    }
    return state
