import streamlit

from inheritscan.tools.classinfo_panel.get_classinfo_markdown import \
    get_detailed_class_description
from inheritscan.tools.classinfo_panel.open_class_in_vscode import \
    open_selected_file_in_vscode


def render_bottom_right(context):
    # define layout
    header = streamlit.container()
    button1, button2 = streamlit.columns(2)
    content_area = streamlit.container()

    # render components
    with header:
        streamlit.markdown("### 📝 Detailed class description")

    with button1:
        b1_handle = streamlit.button(
            "Show Class Details", use_container_width=True
        )
    with button2:
        b2_handle = streamlit.button("Go to VSCODE", use_container_width=True)

    # define actions
    if b1_handle:
        markdown_text = get_detailed_class_description(context)
        streamlit.session_state.rerender_classdetails_content = markdown_text

    if b2_handle:
        open_selected_file_in_vscode(context)

    with content_area:
        content = streamlit.session_state.get(
            "rerender_classdetails_content", ""
        )
        streamlit.markdown(content)
