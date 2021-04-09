from dataclasses import dataclass


@dataclass
class Action:
    display_name: str  # Name to display in UI
    name: str  # Django view name
    url: str  # POST endpoint to execute action
