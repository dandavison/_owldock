from typing import List, Optional, Union

from app.api.serializers import MoveSerializer
from immigration.models import (
    Move,
    Process,
    ProcessRuleSet,
    ProcessStep,
)


def get_processes(move: Union[Move, MoveSerializer]) -> List[Process]:
    """
    Return a list of processes that could be used to effect this move.
    """
    print(f"get_processes() for {move}")
    matching_processes = []
    for process_ruleset in _get_all_process_rule_sets():
        print(f"Considering {process_ruleset}")
        process = _make_process_for_move(process_ruleset, move)
        if process:
            print("Matches!")
            matching_processes.append(process)
    return matching_processes


def _make_process_for_move(
    process_ruleset: ProcessRuleSet, move: Move
) -> Optional[Process]:
    """
    If the move satisfies the process rule, then return the resulting process.
    """
    for predicate in process_ruleset.get_predicates():
        result = predicate(move)
        print(f"    predicate {predicate.__name__} => {result}")
        if not result:
            return None
    steps = []
    for step in _get_all_steps_for_process_rule_set(process_ruleset):
        if step.is_required_for_move(move):
            steps.append(step)
    return Process(route=process_ruleset.route, steps=steps)


def _get_all_process_rule_sets() -> List[ProcessRuleSet]:
    return list(ProcessRuleSet.objects.all())


def _get_all_steps_for_process_rule_set(
    process_ruleset: ProcessRuleSet,
) -> List[ProcessStep]:
    return list(process_ruleset.processstep_set.all())
