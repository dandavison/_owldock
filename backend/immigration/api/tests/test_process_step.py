from immigration.api.models import _prefetch_process_steps_for_host_country_code
from immigration.models import ProcessStep


def test_depends_on_prefetching(
    greece_issuance_of_residence_card_step: ProcessStep,
    greece_biometrics_step: ProcessStep,
):
    depender, dependee = greece_issuance_of_residence_card_step, greece_biometrics_step
    depender.depends_on.add(dependee)
    assert depender.host_country
    prefetched_depender = _prefetch_process_steps_for_host_country_code(
        depender.host_country.code
    )[depender.id]
    assert list(depender.depends_on.all()) == [dependee]
    assert prefetched_depender._prefetched_depends_on == [dependee.id]
