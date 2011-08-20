    
def prune(lst, blacklst):
    """
    Prune a list so it doesn't contain any words within a blacklist of
    stop words
    """
    return [word.lower() for word in lst if isinstance(word, basestring) and not word.lower() in blacklst]
