"""
global_utils.py file for ai4collab app. Global util functions for ai4collab project.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

# ------------- [Functions] -------------

# Function to format message to green with prefix newline.
def green_success(message: string) -> string:
    return f'\n\033[92m {message} \033[0m'

# Function to format message to yellow with prefix newline.
def yellow_warning(message: string) -> string:
    return f'\n\033[93m {message} \033[0m'

# Function to format message to red with prefix newline.
def red_critical(message: string) -> string:
    return f'\n\033[91m {message} \033[0m'
