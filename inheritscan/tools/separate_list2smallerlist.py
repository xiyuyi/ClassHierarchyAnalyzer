def separate_list(lst, chunk_size=5):
    """Divide a list into chunks of size 'chunk_size'."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]