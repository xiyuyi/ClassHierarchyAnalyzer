from inheritscan.tools.ai_summaries import generate_ai_summaries
from inheritscan.tools.parse_subgraph_selected_nodes import get_mod_class_method_list
from inheritscan.tools.render_class_uml import render_detailed_class_uml
from inheritscan.tools.separate_list2smallerlist import separate_list
from inheritscan.tools.streamlit.page.bottomleft_aisumgen_and_render import summaries_generation_and_render


def render_bottom_left(context, streamlit):
    header = streamlit.markdown("### 🔍 Detailed Class View")
    button1 = streamlit.button("🔁 Generate AI summaries", use_container_width=True)

    # Button triggers backend process
    if button1:
        streamlit.session_state["generate_ai_summaries"] = True # Reset the trigger flag
        streamlit.session_state["ai_summary_progress"] = 0  # Reset progress

        # If generation is triggered, run process and show progress
        if streamlit.session_state.get("generate_ai_summaries", False):
            progress_bar = streamlit.progress(0, text="Generating AI summaries...")
            summaries_generation_and_render(progress_bar, streamlit, context)
            streamlit.session_state["generate_ai_summaries"] = False  # Reset the trigger flag

    # Render the panel normally
    uml_diagram_container = streamlit.container()
    with uml_diagram_container:
        if streamlit.session_state.get("render_uml_diagram", True):
            result = render_detailed_class_uml(context)
            if result:
                streamlit.session_state.update(result)