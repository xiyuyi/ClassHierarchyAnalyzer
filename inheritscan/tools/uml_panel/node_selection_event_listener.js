
console.log("✅ JS: Adding Pyvis event listener... ");

window.network.on("select", function(params) {
    console.log("🟢 Node selected:", params.nodes);
    const selectedNodes = params.nodes;
    const nodeData = selectedNodes.map(nodeId => {
        const node = window.network.body.data.nodes.get(nodeId);
        console.log("👉 Full node object for ID:", nodeId, node);
        return {
            id: nodeId,
            full_mod: node.full_mod
        };
    });
    fetch("http://localhost:5555/receive_the_clicked_node_detailed_uml", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nodes: nodeData })
    });
});
