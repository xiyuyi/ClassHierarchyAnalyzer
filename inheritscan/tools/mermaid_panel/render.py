import streamlit


def get_mermaid_html(mermaid_scripts: str):
    html_code = f"""
    <div id="mermaid-container">
        <div class="mermaid">
        {mermaid_scripts}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        // Ensure Mermaid only initializes after the DOM and script are fully ready
        window.addEventListener("load", () => {{
            if (window.mermaid) {{
                try {{
                    mermaid.initialize({{ startOnLoad: false }});
                    mermaid.init(undefined, document.querySelectorAll(".mermaid"));
                }} catch (e) {{
                    console.error("❌ Mermaid render error:", e);
                    const container = document.getElementById("mermaid-container");
                    if (container) {{
                        container.innerHTML = "<pre style='color:red;'>Mermaid render failed:<br>" + e.message + "</pre>";
                    }}
                }}
            }} else {{
                console.error("❌ Mermaid script did not load.");
            }}
        }});
    </script>
    """
    return html_code


def render_mermaid_graph(mermaid_scripts: str):
    html_code = get_mermaid_html(mermaid_scripts)
    streamlit.components.v1.html(html_code, height=800, scrolling=False)
