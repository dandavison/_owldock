import json
from pprint import pprint
from threading import local

from clint.textui import colored
from deepdiff import DeepDiff
from django.dispatch import receiver
from django_fsm.signals import post_transition
from django_fsm.signals import pre_transition

THREAD_LOCALS = local()


@receiver(pre_transition)
def handle_django_fsm_pre_transition(sender, **kwargs):
    from app.http_api.serializers import CaseStepSerializer

    print(colored.black("django_fsm pre_transition signal:", bold=True))
    pprint(kwargs)
    print("\n")
    THREAD_LOCALS.pre_transition_data = CaseStepSerializer(kwargs["instance"]).data


@receiver(post_transition)
def handle_django_fsm_post_transition(sender, **kwargs):
    from app.http_api.serializers import CaseStepSerializer

    print(colored.black("django_fsm post_transition signal:", bold=True))
    pprint(kwargs)
    print("\n")
    THREAD_LOCALS.post_transition_data = CaseStepSerializer(kwargs["instance"]).data

    before = getattr(THREAD_LOCALS, "pre_transition_data", None)
    after = getattr(THREAD_LOCALS, "post_transition_data", None)
    if before and after:
        print_delta(before, after)


def print_delta(before: dict, after: dict) -> None:
    diff = DeepDiff(before, after)
    print(colored.black("Δ", bold=True))
    print(diff)
