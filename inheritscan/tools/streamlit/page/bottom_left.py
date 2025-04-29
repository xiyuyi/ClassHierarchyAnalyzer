from inheritscan.tools.streamlit.page.bottomleft_aisumgen_and_render import (
    summaries_generation_and_render,
)
import streamlit
from inheritscan.tools.uml_panel.entry import render_class_uml


def render_bottom_left(context):
    # define layout:
    header = streamlit.container()
    button1 = streamlit.container() # generate ai summaries
    # Button triggers backend process
    if button1:
        streamlit.session_state["generate_ai_summaries"] = (
            True  # Reset the trigger flag
        )
        streamlit.session_state["ai_summary_progress"] = 0  # Reset progress

        # If generation is triggered, run process and show progress
        if streamlit.session_state.get("generate_ai_summaries", False):
            progress_bar = streamlit.progress(0, text="Generating AI summaries...")
            summaries_generation_and_render(progress_bar, context)
            streamlit.session_state["generate_ai_summaries"] = (
                False  # Reset the trigger flag
            )
    graph_display = streamlit.container()
    # render each element:
    with header:
        streamlit.markdown("### 🔍 Detailed Class View")
    
    with button1:
        streamlit.button("🔁 Generate AI summaries", use_container_width=True)
    


    # Render the panel normally
    with graph_display:
        uml_diagram_container = streamlit.container()
        with uml_diagram_container:
            if streamlit.session_state.get("render_uml_diagram", True):
                streamlit.markdown("### 🗺️ Class Hierarchy Diagram")
                result = render_class_uml(context)
                print("finished rendering class uml, result:")
                print(result)
                if result:
                    streamlit.session_state.update(result)



