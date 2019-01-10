import re

def file_is_of_type(filePath, fileType):
    if filePath.split('.')[1] == fileType:
        return True
    else:
        return False

def get_file_type(filePath):
    return filePath.split('.')[-1]

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
