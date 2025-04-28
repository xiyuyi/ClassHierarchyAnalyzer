from inheritscan.tools.classinfo_panel.get_classinfo_markdown import get_detailed_class_description
from inheritscan.tools.streamlit.page.bottomleft_aisumgen_and_render import (
    summaries_generation_and_render,
)
import streamlit
from inheritscan.tools.uml_panel.entry import render_class_uml


def render_bottom_right(context):
    streamlit.markdown("### 📝 Detailed class description")
    button1 = streamlit.button("Go to VSCODE", use_container_width=True)
    
    markdown_text = get_detailed_class_description(context)

    # Render the markdown string
    streamlit.markdown(markdown_text)

    if button1:
        # TODO open the module for this class in vscode.
        pass