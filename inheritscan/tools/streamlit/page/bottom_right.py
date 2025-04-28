from inheritscan.tools.streamlit.page.bottomleft_aisumgen_and_render import (
    summaries_generation_and_render,
)
import streamlit
from inheritscan.tools.uml_panel.entry import render_class_uml


def render_bottom_right(context):
    streamlit.markdown("### 📝 Detailed class description")
    def get_detailed_class_description():
        return """
        
        #### Class: `ClassName`

        **Fully Qualified Name (FQN):** `mod.to.the.class.ClassName`

        ---

        #### 📄 Description:
        > *(Class description goes here)*

        ---

        #### 🛠️ Major Methods:
        - `method_one()` — *(Short summary of what this method does)*
        - `method_two()` — *(Short summary of what this method does)*
        - `method_three()` — *(Short summary of what this method does)*

   """
    markdown_text = get_detailed_class_description()

    # Render the markdown string
    streamlit.markdown(markdown_text)

    # header = streamlit.markdown("### 🔍 Class details")
    # button1 = streamlit.button("🔁 Generate AI summaries", use_container_width=True)

    # # Button triggers backend process
    # if button1:
    #     streamlit.session_state["generate_ai_summaries"] = (
    #         True  # Reset the trigger flag
    #     )
    #     streamlit.session_state["ai_summary_progress"] = 0  # Reset progress

    #     # If generation is triggered, run process and show progress
    #     if streamlit.session_state.get("generate_ai_summaries", False):
    #         progress_bar = streamlit.progress(0, text="Generating AI summaries...")
    #         summaries_generation_and_render(progress_bar, context)
    #         streamlit.session_state["generate_ai_summaries"] = (
    #             False  # Reset the trigger flag
    #         )

    # # Render the panel normally
    # uml_diagram_container = streamlit.container()
    # with uml_diagram_container:

    #     if streamlit.session_state.get("render_uml_diagram", True):
    #         streamlit.markdown("### 🗺️ Class Hierarchy Diagram")
    #         result = render_class_uml(context)
            
    #         if result:
    #             streamlit.session_state.update(result)
    pass