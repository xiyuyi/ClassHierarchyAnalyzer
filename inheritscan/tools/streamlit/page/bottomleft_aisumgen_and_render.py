from inheritscan.tools.ai_summaries import generate_ai_summaries
from inheritscan.tools.parse_subgraph_selected_nodes import get_mod_class_method_list
from inheritscan.tools.separate_list2smallerlist import separate_list


def summaries_generation_and_render(progress_bar, streamlit, context):
    mod_class_method_list = get_mod_class_method_list(context)
    task_lists = separate_list(mod_class_method_list, chunk_size=5)
    L = len(task_lists)
    for i, tasks_dlist in enumerate(task_lists):
        print("currently handling: ")
        for t in tasks_dlist:
            print("   " + str(t))
        tasks = [(d["mod"], d["class_name"], d["method"]) for d in tasks_dlist]
        generate_ai_summaries(tasks)
        streamlit.session_state["ai_summary_progress"] = i + 1
        progress_bar.progress(
            (i + 1) / L, text=f"Generating AI summaries... {(i+1)/L*100}%"
        )
    streamlit.success("AI summaries generated!")