from typing import Dict

from immigration.api.models import _prefetch_process_steps_for_host_country_code
from immigration.models import ProcessStep


def test_depends_on_prefetching_within_country(
    greece_issuance_of_residence_card_step: ProcessStep,
    greece_biometrics_step: ProcessStep,
):
    depender, dependee = greece_issuance_of_residence_card_step, greece_biometrics_step
    depender.depends_on.add(dependee)

    assert list(depender.depends_on.all()) == [dependee]

    assert depender.host_country
    prefetched_depender = _prefetch_process_steps_for_host_country_code(
        depender.host_country.code
    )[depender.id]

    assert prefetched_depender._prefetched_depends_on == [dependee]


def test_depends_on_prefetching_with_global_step_linear_dependency_chain_1(
    greece_issuance_of_residence_card_step: ProcessStep,
    greece_biometrics_step: ProcessStep,
    brazil_step: ProcessStep,
    france_step: ProcessStep,
    entry_step: ProcessStep,
):
    step_B, step_C = (
        greece_issuance_of_residence_card_step,
        greece_biometrics_step,
    )
    entry_step.depends_on.add(step_B)
    step_B.depends_on.add(step_C)

    assert step_B.host_country and step_C.host_country and not entry_step.host_country
    assert step_B.host_country == step_C.host_country
    prefetched = _prefetch_process_steps_for_host_country_code(step_B.host_country.code)

    assert set(entry_step.depends_on.all()) == {step_B, brazil_step, france_step}
    assert set(step_B.depends_on.all()) == {step_C}
    assert set(step_C.depends_on.all()) == set()

    assert set(prefetched[entry_step.id]._prefetched_depends_on) == {step_B}
    assert set(prefetched[step_B.id]._prefetched_depends_on) == {step_C}
    assert set(prefetched[step_C.id]._prefetched_depends_on) == set()


def test_depends_on_prefetching_with_global_step_linear_dependency_chain_2(
    greece_issuance_of_residence_card_step: ProcessStep,
    greece_biometrics_step: ProcessStep,
    brazil_step: ProcessStep,
    france_step: ProcessStep,
    entry_step: ProcessStep,
):
    step_A, step_C = (
        greece_issuance_of_residence_card_step,
        greece_biometrics_step,
    )
    step_A.depends_on.add(entry_step)
    entry_step.depends_on.add(step_C)

    assert step_A.host_country and step_C.host_country and not entry_step.host_country
    assert step_A.host_country == step_C.host_country
    prefetched = _prefetch_process_steps_for_host_country_code(step_A.host_country.code)

    assert set(step_A.depends_on.all()) == {entry_step}
    assert set(entry_step.depends_on.all()) == {step_C, brazil_step, france_step}
    assert set(step_C.depends_on.all()) == set()

    assert set(prefetched[step_A.id]._prefetched_depends_on) == {entry_step}
    assert set(prefetched[entry_step.id]._prefetched_depends_on) == {step_C}
    assert set(prefetched[step_C.id]._prefetched_depends_on) == set()


def test_depends_on_prefetching_with_global_step_non_linear_dependency_chain(
    greece_issuance_of_residence_card_step: ProcessStep,
    greece_biometrics_step: ProcessStep,
    brazil_step: ProcessStep,
    france_step: ProcessStep,
    entry_step: ProcessStep,
):
    step_A, step_C = (
        greece_issuance_of_residence_card_step,
        greece_biometrics_step,
    )
    step_A.depends_on.add(entry_step, step_C)
    entry_step.depends_on.add(step_C)

    assert step_A.host_country and step_C.host_country and not entry_step.host_country
    assert step_A.host_country == step_C.host_country
    prefetched = _prefetch_process_steps_for_host_country_code(step_A.host_country.code)

    assert set(step_A.depends_on.all()) == {entry_step, step_C}
    assert set(entry_step.depends_on.all()) == {step_C, brazil_step, france_step}
    assert set(step_C.depends_on.all()) == set()

    assert set(prefetched[step_A.id]._prefetched_depends_on) == {entry_step, step_C}
    assert set(prefetched[entry_step.id]._prefetched_depends_on) == {
        step_C,
    }
    assert set(prefetched[step_C.id]._prefetched_depends_on) == set()
