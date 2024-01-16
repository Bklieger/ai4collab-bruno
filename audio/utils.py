"""
utils.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

# Used in Consumers.py. Return empty string if string is None, 
# otherwise return original string.
def empty_string_if_none(string: str) -> str:
    """
    Return empty string if string is None, otherwise return original string.

    Args:
        string (string): String to check.
    
    Returns:
        string: Empty string if string is None, otherwise original string.
    """
    if string == None:
        return ""
    else:
        return string
