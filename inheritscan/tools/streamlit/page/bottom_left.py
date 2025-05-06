from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import streamlit

from inheritscan.tools.streamlit.page.bottomleft_aisumgen_and_render import \
    get_summaries_and_render
from inheritscan.tools.uml_panel.entry import render_class_uml


def render_bottom_left(context):
    # define layout:
    header = streamlit.container()
    button1 = streamlit.container()
    progress = streamlit.container()
    graph_display = streamlit.container()

    # render each component:
    with header:
        streamlit.markdown("### 🔍 Detailed Class View")

    with button1:
        b1_handle = streamlit.button(
            "🔁 Get AI summaries", use_container_width=True
        )

    with progress:
        progress_bar = streamlit.progress(0, text="Getting AI summaries...")

    with graph_display:
        streamlit.markdown("### 🗺️ Class Hierarchy Diagram")
        result = render_class_uml(context)
        print("finished rendering class uml, result:")
        print(result)
        if result:
            streamlit.session_state.update(result)

    # define actions
    if b1_handle:
        print("pressed the 🔁 Get AI summaries button!")
        streamlit.session_state["get_ai_summaries"] = (
            True  # Reset the trigger flag
        )
        streamlit.session_state["ai_summary_progress"] = 0  # Reset progress

        # If generation is triggered, run process and show progress
        if streamlit.session_state.get("get_ai_summaries", False):
            get_summaries_and_render(progress_bar, context)
            streamlit.session_state["get_ai_summaries"] = (
                False  # Reset the trigger flag
            )
