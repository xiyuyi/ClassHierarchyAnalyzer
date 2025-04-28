from inheritscan.tools.streamlit.page.bottomleft_aisumgen_and_render import (
    summaries_generation_and_render,
)
import streamlit
from inheritscan.tools.uml_panel.entry import render_class_uml


def render_bottom_right(context):
    button1 = streamlit.button("Go to VSCODE", use_container_width=True)
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

    if button1:
        # TODO open the module for this class in vscode.
        pass