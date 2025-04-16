from pyvis.network import Network
def get_class_hierarchy_pyvis_network(nx_graph):
    pyvis_g = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
    for node in nx_graph.nodes(data=True):
        full_mod = node[0][0] + "." + node[0][1]        
        # mod = node[1].get("class_name", "EMPTY")
        pyvis_g.add_node(node[0][1], title=full_mod)

    for edge in nx_graph.edges():
        print(edge)
        pyvis_g.add_edge(edge[0][1], edge[1][1], arrows="to")

    return pyvis_g