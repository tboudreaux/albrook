import re

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    return l


def clear_lists(l1, l2):
    newl1 = [x for x in l1 if x != None]
    newl2 = [x for i, x in enumerate(l2) if l1[i] != None]
    return newl1, newl2