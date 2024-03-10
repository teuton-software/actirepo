
def format_bytes(size):
    """
    Convert bytes to human readable format
    """
    power = 2**10
    n = 0
    power_labels = { 0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB' }
    while size > power:
        size /= power
        n += 1
    return f"{size:.0f} {power_labels[n]}"

def title(text):
    """
    Print title
    """
    size = len(text)
    print()
    print("=" * size)
    print(text)
    print("=" * size)