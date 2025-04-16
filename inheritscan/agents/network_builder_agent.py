import networkx as nx

class NetworkBuilderAgent:
    def __call__(self, state: dict) -> dict:
        """
        This function would execute when user calls invoke()
        it should modify the state dictionary.
        """

        # add class inheritance hierarchy graph
        G = nx.DiGraph()
        for ic in state['internal_classes']:
            G.add_node(ic, class_name = ic[1])

        mods=list(state['modules_details'].keys())
        for mod in mods:
            if 'class_inheritances' in state['modules_details'][mod]:
                ch = state['modules_details'][mod]['class_inheritances']
                for node in ch:
                    for child in ch[node]['inherits']:
                        G.add_edge(node, child, relation='inherits')

        state['class_hierachy_network_graph'] = G
        return state
    
