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
        to_addresses = [self.provider_contact.user.email]
        from_address = "owldock@owldock.com"
        subject = "Owldock: your services have been requested"
        content = dedent(
            f"""The following steps of case {case.uuid} have been offered to you:
        {step_names}

        (TODO: Describe next actions provider should take)
        """
        )
        raise Exception(
            f"TODO: sending email is not implemented yet. The following email would have been sent:"
            f"    To:      {', '.join(to_addresses)}\n",
            f"    From:    {from_address}\n",
            f"    Subject: {subject}\n",
            f"    Content: {content}\n",
        )
        send_mail(
            subject,
            content,
            from_address,
            to_addresses,
            fail_silently=False,
        )
