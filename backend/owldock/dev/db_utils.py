import sys
from contextlib import ExitStack
from contextlib import contextmanager

from django.db import connections
from django.test.utils import CaptureQueriesContext


@contextmanager
def assert_n_queries(expected: int):
    with ExitStack() as stack:
        capturers = {
            cxn.alias: stack.enter_context(CaptureQueriesContext(cxn))
            for cxn in connections.all()
        }
        yield
        n_queries = sum(len(c.captured_queries) for c in capturers.values())
        if n_queries != expected:
            for name, capturer in capturers.items():
                print(name, file=sys.stdout)
                for query in capturer.captured_queries:
                    print(f"    {query}", file=sys.stdout)
            raise AssertionError(f"Expected {expected} queries; saw {n_queries}")


@contextmanager
def print_queries():
    with ExitStack() as stack:
        capturers = {
            cxn.alias: stack.enter_context(CaptureQueriesContext(cxn))
            for cxn in connections.all()
        }
        yield

        print("Queries:")
        for alias, capturer in capturers.items():
            print(f"    {alias}: {len(capturer.captured_queries)}")
