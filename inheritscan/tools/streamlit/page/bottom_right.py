import streamlit

from inheritscan.tools.classinfo_panel.get_classinfo_markdown import \
    get_detailed_class_description
from inheritscan.tools.classinfo_panel.open_class_in_vscode import \
    open_selected_file_in_vscode


def render_bottom_right(context):
    streamlit.markdown("### 📝 Detailed class description")
    b1, b2 = streamlit.columns(2)
    with b1:
        button1 = streamlit.button(
            "Show Class Details", use_container_width=True
        )
    with b2:
        button2 = streamlit.button("Go to VSCODE", use_container_width=True)

    if button1:
        streamlit.session_state.rerender_classdetails_view = True
        markdown_text = get_detailed_class_description(context)
        streamlit.session_state.rerender_classdetails_content = markdown_text

    content = streamlit.session_state.rerender_classdetails_content
    streamlit.markdown(content)

    if button2:
        # TODO open the module for this class in vscode.
        # Consider extracting `mod` and `class_name` from context or JSON
        open_selected_file_in_vscode(context)
