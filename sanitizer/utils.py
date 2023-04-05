import bleach

def is_bleach_version_5():
    return int(bleach.__version__.split(".")[0]) >=5