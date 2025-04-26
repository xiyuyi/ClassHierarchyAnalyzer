def format_class_label(class_name, methods):
    
    maxlen = max(len(class_name), 0)
    
    for method in methods:
        maxlen = max(maxlen, len(method))

    line_sep = "_"*maxlen
    methods_text = "\n".join([f"  {m}()" for m in methods])
    return f"<class>\n{class_name}\n{line_sep}\n{methods_text}"