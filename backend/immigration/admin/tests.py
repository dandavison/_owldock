from dataclasses import dataclass

import pytest
import sqlparse
from django.contrib.admin.sites import AdminSite

from immigration.admin import ProcessStepAdmin
from immigration.models import ProcessStep
from immigration.tests import factories
from owldock.dev.db_utils import assert_max_queries, print_query_counts
from owldock.tests.constants import TEST_PASSWORD


class MockSuperUser:
    def has_perm(self, perm):
        return True


@dataclass
class MockRequest:
    user: MockSuperUser


def test_processruleset_admin_view_queries(
    greece_local_hire_article_17_rule_set,
    admin_user_client,
):
    id = greece_local_hire_article_17_rule_set.id
    with assert_max_queries(20):
        admin_user_client.get(
            f"/admin/immigration/processruleset/{id}/change/", follow=True
        )


def test_processruleset_admin_list_view_queries(
    greece_local_hire_article_17_rule_set,
    admin_user_client,
):
    with assert_max_queries(20):
        admin_user_client.get("/admin/immigration/processruleset/", follow=True)


@pytest.mark.skip
def test_process_step_issued_document_type_choices():
    admin = ProcessStepAdmin(model=ProcessStep, admin_site=AdminSite())
    request = MockRequest(user=MockSuperUser())

    process_step = factories.ProcessStepFactory()
    id_inline, si_inline = admin.get_inline_instances(request, process_step)
    form = id_inline._get_form_for_get_fields(request, process_step)
    query = form.base_fields["issued_document_type"].queryset.query
    print(sqlparse.format(str(query), reindent=True))
