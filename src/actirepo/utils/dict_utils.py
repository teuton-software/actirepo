"""
Utility functions for working with dictionaries
- trim_all_keys: Trim keys from a list of dictionaries
- trim_keys: Trim keys from a dictionary
"""

def trim_all_keys(dict, keys):
    """
    Trim keys from a list of dictionaries    
    """
    return [ trim_keys(x, keys) for x in dict ]

def trim_keys(dict, keys):
    """
    Trim keys from a dictionary
    """
    return {k: dict[k] for k in keys}