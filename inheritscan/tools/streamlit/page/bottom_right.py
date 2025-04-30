import streamlit

from inheritscan.tools.classinfo_panel.get_classinfo_markdown import \
    get_detailed_class_description


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
        markdown_text = get_detailed_class_description(context)
        streamlit.markdown(markdown_text)

    if button2:
        # TODO open the module for this class in vscode.
        # Consider extracting `mod` and `class_name` from context or JSON
        # open_selected_file_in_vscode(contex)
        pass
