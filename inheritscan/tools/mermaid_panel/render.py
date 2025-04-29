import streamlit


def get_mermaid_html(mermaid_scripts: str):
    html_code = f"""
    <div class="mermaid">
    {mermaid_scripts}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{startOnLoad:true}});

        function callNodeClick(nodeId) {{
            console.log("✅ Node clicked:", nodeId);
            alert("You clicked node: " + nodeId);
        }}
    </script>
    """
    return html_code


def render_mermaid_graph(mermaid_scripts: str):
    html_code = get_mermaid_html(mermaid_scripts)
    streamlit.components.v1.html(html_code, height=500)
