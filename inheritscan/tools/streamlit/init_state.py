from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)


def initialize_session_state(streamlit):
    if "selected_cluster" not in streamlit.session_state:
        streamlit.session_state.selected_cluster = None

    if "selected_classes" not in streamlit.session_state:
        streamlit.session_state.selected_classes = []

    if "selected_class_detail" not in streamlit.session_state:
        streamlit.session_state.selected_class_detail = None

    if "class_hierarchy_network_graph" not in streamlit.session_state:
        streamlit.session_state.class_hierarchy_network_graph = None

    if "modules_name2path" not in streamlit.session_state:
        streamlit.session_state.modules_name2path = None

    if "modules_details" not in streamlit.session_state:
        streamlit.session_state.modules_details = None

    if "detailed_uml_class_graph" not in streamlit.session_state:
        streamlit.session_state.detailed_uml_class_graph = None

    if "detailed_nx_graph" not in streamlit.session_state:
        streamlit.session_state.detailed_nx_graph = None

    # initialize re-render flag
    if "rerender_sub_graph" not in streamlit.session_state:
        streamlit.session_state.rerender_sub_graph = False

    if "rerender_uml_view" not in streamlit.session_state:
        streamlit.session_state.rerender_uml_view = False

    if "rerender_classdetails_view" not in streamlit.session_state:
        streamlit.session_state.rerender_classdetails_view = False
