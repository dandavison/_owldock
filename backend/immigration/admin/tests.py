from dataclasses import dataclass

from django.contrib.admin.sites import AdminSite
import sqlparse

from immigration.admin import ProcessStepAdmin
from immigration.models import ProcessStep
from immigration.tests import factories


class MockSuperUser:
    def has_perm(self, perm):
        return True


@dataclass
class MockRequest:
    user: MockSuperUser


@pytest.mark.skip
def test_process_step_issued_document_type_choices():
    admin = ProcessStepAdmin(model=ProcessStep, admin_site=AdminSite())
    request = MockRequest(user=MockSuperUser())

    process_step = factories.ProcessStepFactory()
    id_inline, si_inline = admin.get_inline_instances(request, process_step)
    form = id_inline._get_form_for_get_fields(request, process_step)
    query = form.base_fields["issued_document_type"].queryset.query
    print(sqlparse.format(str(query), reindent=True))
