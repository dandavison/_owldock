import json
from copy import deepcopy
from django.test import Client as DjangoTestClient
from typing import List, Set

from immigration.models import ProcessRuleSet, ProcessStep


def test_gantt_chart_noop(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    admin_user_client: DjangoTestClient,
):
    client = admin_user_client
    process = greece_local_hire_article_17_rule_set
    serialized_process = _serialize_process(process)
    response = client.post(
        f"/api/process/{process.id}/",
        json.dumps(serialized_process),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert _serialize_process(process) == serialized_process


def test_gantt_chart_update_duration(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    admin_user_client: DjangoTestClient,
):
    client = admin_user_client
    process = greece_local_hire_article_17_rule_set
    original_serialized_process = _serialize_process(process)
    serialized_process = deepcopy(original_serialized_process)
    [step] = [
        s
        for s in serialized_process
        if s["id"] == process.step_rulesets[0].process_step.id
    ]
    step["step_duration_range"] = [d + 1 for d in step["step_duration_range"]]
    response = client.post(
        f"/api/process/{process.id}/",
        json.dumps(serialized_process),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert original_serialized_process != serialized_process
    assert _serialize_process(process) == serialized_process


def test_gantt_chart_update_remove_depends_on(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    admin_user_client: DjangoTestClient,
):
    client = admin_user_client
    process = greece_local_hire_article_17_rule_set
    (
        depender,
        dependee_1,
        dependee_2,
        *_,
    ) = ProcessStep.objects.get_for_host_country_codes(
        [process.route.host_country.code]
    )
    depender.depends_on.set([dependee_1, dependee_2])
    original_serialized_process = _serialize_process(process)
    serialized_process = deepcopy(original_serialized_process)
    [step] = [s for s in serialized_process if s["id"] == depender.id]
    assert set(step["depends_on_ids"]) == {dependee_1.id, dependee_2.id}
    step["depends_on_ids"] = [dependee_1.id]
    response = client.post(
        f"/api/process/{process.id}/",
        json.dumps(serialized_process),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert original_serialized_process != serialized_process
    assert _serialize_process(process) == serialized_process


def test_gantt_chart_update_insert_depends_on(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    admin_user_client: DjangoTestClient,
):
    client = admin_user_client
    process = greece_local_hire_article_17_rule_set
    (
        depender,
        dependee_1,
        dependee_2,
        *_,
    ) = ProcessStep.objects.get_for_host_country_codes(
        [process.route.host_country.code]
    )
    depender.depends_on.set([dependee_1])
    original_serialized_process = _serialize_process(process)
    serialized_process = deepcopy(original_serialized_process)
    [step] = [s for s in serialized_process if s["id"] == depender.id]
    assert set(step["depends_on_ids"]) == {dependee_1.id}
    step["depends_on_ids"].append(dependee_2.id)
    step["depends_on_ids"].sort()
    response = client.post(
        f"/api/process/{process.id}/",
        json.dumps(serialized_process),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert original_serialized_process != serialized_process
    assert _serialize_process(process) == serialized_process


def test_gantt_chart_remove_step(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    admin_user_client: DjangoTestClient,
):
    client = admin_user_client
    process = greece_local_hire_article_17_rule_set
    original_serialized_process = _serialize_process(process)
    serialized_process = [
        s
        for s in original_serialized_process
        if s["id"] != process.step_rulesets[0].process_step.id
    ]
    response = client.post(
        f"/api/process/{process.id}/",
        json.dumps(serialized_process),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert original_serialized_process != serialized_process
    assert _serialize_process(process) == serialized_process


def test_gantt_chart_insert_step(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    greece_tax_registration_step: ProcessStep,
    admin_user_client: DjangoTestClient,
):
    # The new step was not involved in this process previously, but it does have
    # a dependency on a step in this process. We must ensure that we do not
    # treat the absence of this dependency in the POST data as a request to
    # delete this dependency, since the dependency is a valid dependency but in
    # a different process.
    greece_tax_registration_step.depends_on.set(
        [greece_local_hire_article_17_rule_set.step_rulesets[0].process_step]
    )
    _gantt_chart_insert_step(
        process=greece_local_hire_article_17_rule_set,
        new_step=greece_tax_registration_step,
        client=admin_user_client,
        with_dependees=False,
    )


def test_gantt_chart_insert_step_with_dependees(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    greece_tax_registration_step: ProcessStep,
    admin_user_client: DjangoTestClient,
):
    _gantt_chart_insert_step(
        process=greece_local_hire_article_17_rule_set,
        new_step=greece_tax_registration_step,
        client=admin_user_client,
        with_dependees=True,
    )


def test_gantt_chart_insert_entry_step(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    entry_step: ProcessStep,
    admin_user_client: DjangoTestClient,
):
    original_entry_step_depends_on = set(entry_step.depends_on.all())
    _gantt_chart_insert_step(
        process=greece_local_hire_article_17_rule_set,
        new_step=entry_step,
        client=admin_user_client,
        with_dependees=False,
    )
    entry_step_depends_on = set(entry_step.depends_on.all())
    assert entry_step_depends_on == original_entry_step_depends_on


def test_gantt_chart_insert_entry_step_with_dependees(
    greece_local_hire_article_17_rule_set: ProcessRuleSet,
    entry_step: ProcessStep,
    admin_user_client: DjangoTestClient,
):
    original_entry_step_depends_on = set(entry_step.depends_on.all())
    _gantt_chart_insert_step(
        process=greece_local_hire_article_17_rule_set,
        new_step=entry_step,
        client=admin_user_client,
        with_dependees=True,
    )
    entry_step_depends_on = set(entry_step.depends_on.all())
    assert entry_step_depends_on > original_entry_step_depends_on


def _gantt_chart_insert_step(
    process: ProcessRuleSet,
    new_step: ProcessStep,
    client: DjangoTestClient,
    with_dependees: bool,
):
    original_serialized_process = _serialize_process(process)
    step_ids = {s.process_step.id for s in process.step_rulesets}
    assert new_step.id not in step_ids
    assert (
        not new_step.host_country or new_step.host_country == process.route.host_country
    )
    serialized_process = original_serialized_process + [
        _serialize_step(new_step, step_ids)
    ]
    if with_dependees:
        *serialized_steps, serialized_new_step = serialized_process
        assert not serialized_new_step["depends_on_ids"]
        serialized_new_step["depends_on_ids"] = [serialized_steps[0]["id"]]

    response = client.post(
        f"/api/process/{process.id}/",
        json.dumps(serialized_process),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert original_serialized_process != serialized_process
    assert _serialize_process(process) == serialized_process


def _serialize_process(process: ProcessRuleSet) -> List[dict]:
    step_ids = {s.process_step.id for s in process.step_rulesets}
    return [_serialize_step(sr.process_step, step_ids) for sr in process.step_rulesets]


def _serialize_step(step: ProcessStep, step_ids: Set[int]) -> dict:
    return {
        "id": step.id,
        "depends_on_ids": sorted(set(step.depends_on_ids) & step_ids),
        "step_duration_range": [
            step.estimated_min_duration_days,
            step.estimated_max_duration_days,
        ],
    }
