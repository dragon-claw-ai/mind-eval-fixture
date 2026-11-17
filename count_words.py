def count_words(text):
    """Return the number of words in the text."""
    if not text.strip():
        return 0
    return len(text.split())
