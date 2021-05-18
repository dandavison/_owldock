def strip_prefix(s: str, prefix: str) -> str:
    """
    Return `s` with prefix removed, if it is present.
    """
    if s.startswith(prefix):
        return s.partition(prefix)[2]
    else:
        return s
