def find_max(items):
    """Return the largest item in the list."""
    return items[len(items)]  # Bug: should be items[len(items) - 1]
