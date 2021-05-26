import re
import sys
import sqlparse
from collections import Counter
from contextlib import contextmanager, ExitStack

from django.db import connections, router
from django.db.models import QuerySet
from django.db.models.deletion import Collector
from django.test.utils import CaptureQueriesContext


@contextmanager
def assert_max_queries(expected: int):
    with ExitStack() as stack:
        capturers = {  # type: ignore
            cxn.alias: stack.enter_context(CaptureQueriesContext(cxn))  # type: ignore
            for cxn in connections.all()
        }
        yield
        n_queries = sum(len(c.captured_queries) for c in capturers.values())
        if n_queries > expected:
            for name, capturer in capturers.items():
                print(name, file=sys.stdout)
                for query in capturer.captured_queries:
                    print(f"    {query}", file=sys.stdout)
            raise AssertionError(f"Expected {expected} queries; saw {n_queries}")


@contextmanager
def print_query_counts():
    yield from _print_query_info(counts_only=True)


@contextmanager
def print_queries():
    yield from _print_query_info(counts_only=False)


def _print_query_info(counts_only):
    with ExitStack() as stack:
        capturers = {  # type: ignore
            cxn.alias: stack.enter_context(CaptureQueriesContext(cxn))  # type: ignore
            for cxn in connections.all()
        }
        yield

        print("Query counts:" if counts_only else "Queries:")
        for alias, capturer in capturers.items():
            if not counts_only:
                for query in capturer.captured_queries:
                    sql = re.sub("^SELECT .+ FROM", "SELECT * FROM", query["sql"])
                    print(sqlparse.format(sql, reindent=True))
                    print(query["time"])
                    print()
            print(f"    {alias}: {len(capturer.captured_queries)}")


def objects_to_be_deleted(queryset: QuerySet):
    collector = Collector(using=router.db_for_write(queryset.model))
    collector.collect(queryset)
    print("collector.dependencies:")
    for model, dependent_models in collector.dependencies.items():
        print(model, dependent_models)
    print()
    print("collector.fast_deletes:")
    print({qs.model: qs.count() for qs in collector.fast_deletes})
    print()
    print("collector.data:")
    print({k: len(v) for k, v in collector.data.items()})
