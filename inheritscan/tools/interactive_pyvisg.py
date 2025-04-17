import streamlit.components.v1 as components
import tempfile

def interactive_pyvis_graph(net, height=600):
    js = """
    <script type="text/javascript">
        console.log("✅ JS: Pyvis event listener loaded.");
        window.network.on("select", function(params) {
            console.log("🟢 Node selected:", params.nodes);
            const selectedNodes = params.nodes;
            const nodeData = selectedNodes.map(nodeId => {
                const node = window.network.body.data.nodes.get(nodeId);
                return {
                    id: nodeId,
                    full_mod: node.title
                };
            });
            fetch("http://localhost:5555/receive_selection", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({nodes: nodeData})
            });
        });
    </script>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html = open(tmp_file.name, 'r', encoding='utf-8').read()
        html = html.replace(
            "var network = new vis.Network(container, data, options);",
            "var network = new vis.Network(container, data, options); window.network = network;"
        )
        html += js


    # Inject JS to send selected node to Streamlit
    # html_with_callback = html.replace(
    #     "</script>",
    #     """
    #     network.on("selectNode", function(params) {
    #         const selectedNodes = params.nodes;
    #         window.parent.postMessage({
    #             isStreamlitMessage: true,
    #             type: "streamlit:setComponentValue",
    #             value: selectedNodes
    #         }, "*");
    #     });
    #     </script>
    #     """
    # )

    # Display and return selected node from Streamlit frontend
    selected_nodes = components.html(html, height=height, scrolling=True)
    return selected_nodes  

