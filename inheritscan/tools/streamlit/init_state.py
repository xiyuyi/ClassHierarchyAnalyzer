def initialize_session_state(streamlit):
    if "selected_cluster" not in streamlit.session_state:
        streamlit.session_state.selected_cluster = None

    if "selected_classes" not in streamlit.session_state:
        streamlit.session_state.selected_classes = []

    if "selected_class_detail" not in streamlit.session_state:
        streamlit.session_state.selected_class_detail = None

    if "class_hierachy_network_graph" not in streamlit.session_state:
        streamlit.session_state.class_hierachy_network_graph = None

    if "modules_name2path" not in streamlit.session_state:
        streamlit.session_state.modules_name2path = None

    if "modules_details" not in streamlit.session_state:
        streamlit.session_state.modules_details = None
