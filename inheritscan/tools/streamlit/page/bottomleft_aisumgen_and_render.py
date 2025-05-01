import streamlit

from inheritscan.tools.ai_summaries import get_ai_summaries
from inheritscan.tools.parse_subgraph_selected_nodes import \
    get_mod_class_method_list
from inheritscan.tools.separate_list2smallerlist import separate_list


def _get_task_groups(context):
    # TODO #30
    # future version would be to generate task_lists based on whether the summaries for
    # the given task is available or not.
    mod_class_method_list = get_mod_class_method_list(context)
    task_lists = separate_list(mod_class_method_list, chunk_size=5)
    return task_lists


def get_summaries_and_render(progress_bar, context):
    task_lists = _get_task_groups(context)
    L = len(task_lists)
    for i, tasks_dlist in enumerate(task_lists):
        print("currently handling: ")
        for t in tasks_dlist:
            print("   " + str(t))
        tasks = [(d["mod"], d["class_name"], d["method"]) for d in tasks_dlist]

        get_ai_summaries(tasks)

        streamlit.session_state["ai_summary_progress"] = i + 1
        progress_bar.progress(
            (i + 1) / L, text=f"Generating AI summaries... {(i+1)/L*100}%"
        )
    streamlit.success("AI summaries generated!")
