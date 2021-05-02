from typing import List, Optional

from immigration.models import (
    Move,
    Process,
    ProcessRuleSet,
    ProcessStep,
)


def get_processes(move: Move) -> List[Process]:
    """
    Return a list of processes that could be used to effect this move.
    """
    print(f"get_processes() for {move}")
    matching_processes = []
    for process_rule_set in _get_all_process_rule_sets():
        print(f"Considering {process_rule_set}")
        process = _make_process_for_move(process_rule_set, move)
        if process:
            print(f"Matches!")
            matching_processes.append(process)
    return matching_processes


def _make_process_for_move(
    process_rule_set: ProcessRuleSet, move: Move
) -> Optional[Process]:
    """
    If the move satisfies the process rule, then return the resulting process.
    """
    for predicate in process_rule_set.get_predicates():
        result = predicate(move)
        print(f"    predicate {predicate.__name__} => {result}")
        if not result:
            return None
    steps = []
    for step in _get_all_steps_for_process_rule_set(process_rule_set):
        if step.is_required_for_move(move):
            steps.append(step)
    return Process(route=process_rule_set.route, steps=steps)


def _get_all_process_rule_sets() -> List[ProcessRuleSet]:
    return list(ProcessRuleSet.objects.all())


def _get_all_steps_for_process_rule_set(
    process_rule_set: ProcessRuleSet,
) -> List[ProcessStep]:
    return list(process_rule_set.processstep_set.all())
