"""
Global util functions for ai4collab project.
"""

# ------------- [Functions] -------------

# Function to format message to green with prefix newline.
def green_success(message):
    return f'\n\033[92m {message} \033[0m'

# Function to format message to yellow with prefix newline.
def yellow_warning(message):
    return f'\n\033[93m {message} \033[0m'

# Function to format message to red with prefix newline.
def red_critical(message):
    return f'\n\033[91m {message} \033[0m'
