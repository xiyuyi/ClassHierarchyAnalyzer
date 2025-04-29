from pathlib import Path
import inheritscan
import json

from inheritscan.storage.runtime_json.runtime_json_dumpers import dump_global_inheritance_graph
class GraphManager:
        
    @classmethod
    def write_global_graph(cls, nx_global):
        runtime_folder = Path(inheritscan.__file__).parent.parent / ".run_time"
        meta_fpath = runtime_folder / "meta.json"

        with open(meta_fpath,'r') as f:
            data = json.load(f)
        package_name = data[0]['package_name']

        # use FQN as the key for each class. 
        class_table = {}
        for node in nx_global.nodes:
            fqn = package_name + '.' + '.'.join(node)
            class_table[fqn] = []

        for edge in nx_global.edges:
            fqn_parent = package_name + '.' + '.'.join(edge[1])
            fqn_child = package_name + '.' + '.'.join(edge[0])
            class_table[fqn_parent].append(fqn_child)

        dump_global_inheritance_graph(class_table)
        print(runtime_folder)
        # save global graph inforamtion to json archive. 
        pass

