import json
import os
import tempfile


def load_selected_subgraph_ids(
    path=".run_time/selected_nodes_subgraph.json",
):
    if os.path.exists(path):
        with open(path, "r") as f:
            selected_data = json.load(f)
        # node.id is the Pyvis node ID
        return [item["id"] for item in selected_data]
    return []


def build_interactive_pyvis_subgraph_html(net):
    selected_ids = load_selected_subgraph_ids()
    selected_ids_json = json.dumps(selected_ids)  # safe for JS embedding
    js = """
    <script type="text/javascript">
        console.log("✅ JS: Pyvis event listener loaded.");

        // 🎯 fetch selected nodes
        function applyInitialNodeColorsFromFlask() {
            fetch("http://localhost:5555/selected_nodes_subgraph.json")
                .then(res => res.json())
                .then(selectedNodes => {
                    console.log("👀 Raw selectedNodes from Flask:", selectedNodes);
                    const selectedIds = selectedNodes.map(n => n.id);
                    const allNodes = window.network.body.data.nodes.get();

                    console.log("👀 All node IDs in graph:", allNodes.map(n => n.id));
                    console.log("📦 Selected IDs from Flask:", selectedIds);

                    allNodes.forEach(node => {
                        const isSelected = selectedIds.includes(node.id);
                        if (isSelected) {
                            console.log("🎯 Highlighting node:", node.id);
                        }

                        window.network.body.data.nodes.update({
                            id: node.id,
                            color: {
                            background: isSelected ? "red" : "orange",
                            border: isSelected ? "black" : "#2B7CE9"
                            }
                        });
                    });
                    window.network.unselectAll();
                })
                .catch(err => {
                    console.error("❌ Failed to fetch selected_nodes_subgraph.json:", err);
                });
        }


        setTimeout(applyInitialNodeColorsFromFlask, 500);

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
            fetch("http://localhost:5555/receive_selection_subgraph", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nodes: nodeData })
            }).then(() => {
                applyInitialNodeColorsFromFlask();  // ✅ update highlight
            });
        });
    </script>

    """

    js = js.replace("__SELECTED_IDS__", selected_ids_json)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html = open(tmp_file.name, "r", encoding="utf-8").read()
        html = html.replace(
            "var network = new vis.Network(container, data, options);",
            "var network = new vis.Network(container, data, options); window.network = network;",
        )
        html += js

    return html
