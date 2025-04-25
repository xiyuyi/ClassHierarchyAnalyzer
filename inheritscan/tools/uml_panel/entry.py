import streamlit
import networkx as nx
from inheritscan.tools.uml_panel.render_class_uml import (
    get_detailed_uml_class_graph,
    render_pyvis_class_uml,
)


def render_class_uml(context=None):
    # This is the integration entrypoint for the UML rendering panel in the
    # main Class hierarchy explorer Streamlit app.

    # TODO #7: render detailed UML diagram for the selected classes.
    # with basic summaries displayed with mouse hover event on each node.
    # modify the node's labels for information to be displayed with mouse hover event.

    # TODO #7
    # load nodes information from .run_time/selected_nodes_subgraph.json
    # calculate/retrieve the detailed information for this cluster of nodes
    # save out to .run_time/detailed_uml_info.json
    # Information should be:
    # Aggregate class summaries (class leve, method level, chunks level, everything), and inheritance info.
    # enough to generate diagrams
    # enough to generate mermaid or plantuml codes (need inheritanc einformation?)

    nx_graph: nx.DiGraph = get_detailed_uml_class_graph()
    html = render_pyvis_class_uml(nx_graph)
    streamlit.components.v1.html(html, height=650, scrolling=True)
    # TODO #7
    # need html interaction logic here for node selection.
    # should modify the html code, add javascript and event listening. hook up with flask Post.
    # when a user clikcs on a node, detailed information fo rthe node should be displayed on
    # the bottom right panel.
    # implement after streamlit integration
