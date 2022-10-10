""" Utilities
"""


def truncate_words(text, words=14, orphans=1, suffix="..."):
    """
    Truncate text by number of words. Orphans is the number of trailing
    words not to cut, for example:

    >>> from eea.facetednavigation.utils import truncate_words
    >>> a = 'This is a nice method'
    >>> truncate_words(a, 3, 2)
    'This is a nice method'

    >>> truncate_words(a, 3, 1)
    'This is a...'

    """
    keywords = text.split()
    keywords = [word for word in keywords if word]
    if len(keywords) <= (words + orphans):
        return text
    return " ".join(keywords[:words]) + suffix


def truncate_length(text, length=60, orphans=5, suffix="...", prefix=""):
    """
    Truncate text by number of characters without cutting words at the end.
    Orphans is the number of trailing chars not to cut, for example:

    >>> from eea.facetednavigation.utils import truncate_length
    >>> a = 'This is a nice method'
    >>> truncate_length(a, 19, 2)
    'This is a nice method'

    >>> truncate_length(a, 19, 1)
    'This is a nice...'

    """
    text = " ".join(word for word in text.split() if word)
    if len(text) <= length + orphans:
        return text
    return prefix + " ".join(text[: length + 1].split()[:-1]) + suffix


def truncate(text, words=20, length=160, suffix="..."):
    """
    Split text by given words and length

    >>> from eea.facetednavigation.utils import truncate
    >>> a = ('Fusce neque. Morbi vestibulum volutpat enim. '
    ...      'Vivamus euismod mauris. Donec mollis hendrerit risus. Phasellus a est.')
    >>> truncate(a, 10, 30)
    'Fusce neque. Morbi vestibulum...'

    """
    orphans = int(0.1 * length)  # 10%
    trunk = truncate_length(text, length, orphans, "")

    orphans = int(0.1 * words)  # 10%
    trunk = truncate_words(trunk, words, orphans, "")

    if trunk == text:
        return text

    return trunk + suffix
