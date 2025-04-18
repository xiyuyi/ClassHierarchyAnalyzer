from inheritscan.lcgraphs.class_hierarchy import ClassHierarchyGraphBuilder
from inheritscan.tools.sub_graph import render_sub_graph_panel


state = {
    'codebase_path': '/Users/xiyuyi/github_repos/OpenHands/openhands',
    'module_cluster_levels': 1,
    'package_name': 'openhands'
}
builder = ClassHierarchyGraphBuilder()
class_hierachy_graph = builder.compile_graph()
state = class_hierachy_graph.invoke(state)
nx_graph = state['class_hierachy_network_graph']

context = {"class_hierachy_network_graph": nx_graph}


render_sub_graph_panel(context)