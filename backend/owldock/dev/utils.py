from contextlib import contextmanager
from datetime import datetime


@contextmanager
def print_time():
    t0 = datetime.now()
    yield
    t1 = datetime.now()
    print(t1 - t0)
