from dataclasses import dataclass
from textwrap import dedent
from typing import List

from django.core.mail import send_mail

from app.models import ProviderContact
from client.models import CaseStep


@dataclass
class OfferedCaseStepsNotifier:
    provider_contact: ProviderContact
    case_steps: List[CaseStep]

    def notify(self):
        [case] = [s.case for s in self.case_steps]
        step_names = "- " + "\n- ".join(
            s.process_step.service.name for s in self.case_steps
        )
        message = dedent(
            f"""The following steps of case {case.uuid} have been offered to you:
        {step_names}

        (TODO: Describe next actions provider should take)
        """
        )
        send_mail(
            "Owldock: your services have been requested",
            message,
            "owldock@owldock.com",
            [self.provider_contact.user.email],
            fail_silently=False,
        )
