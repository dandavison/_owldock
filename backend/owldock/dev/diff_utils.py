import json

from difflib import unified_diff
from subprocess import Popen, PIPE


def print_diff(a, b):
    """
    https://github.com/dandavison/delta
    """
    if not (isinstance(a, str) and isinstance(b, str)):
        a = json.dumps(a, sort_keys=True, indent=2)
        b = json.dumps(b, sort_keys=True, indent=2)
    diff = "\n".join(unified_diff(a.splitlines(), b.splitlines()))
    if not diff:
        print("<no change>")
    else:
        proc = Popen(["delta", "--paging", "never"], stdin=PIPE)
        proc.stdin.write(diff.encode("utf-8"))  # type: ignore
        proc.communicate()
