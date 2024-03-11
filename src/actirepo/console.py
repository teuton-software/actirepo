
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

def input_string(name, default_value = None):
    """
    Input string with default value
    """
    value = input(f"{name} [{default_value}]: ")
    if not value:
        value = default_value
    return value

def input_list(name, default_value = None):
    """
    Input comma separated list with default value
    """
    value = input(f"{name} {default_value}: ")
    if not value:
        return default_value
    return [ item.strip() for item in value.split(",") ]