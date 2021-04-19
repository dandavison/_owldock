from dataclasses import dataclass
from textwrap import dedent
from typing import List

from django.core.mail import send_mail

from app.models import ProviderContact
from client.models import CaseStep
from owldock.http import add_message


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
            f"""
            The following steps of case {case.uuid}
            have been offered to you:
            {step_names}

            (TODO: Describe next actions provider should take)
            """
        )
        send_mail(
            subject,
            content,
            from_address,
            to_addresses,
            fail_silently=False,
        )
        add_message(
            (
                "Owldock does not actually send email yet.<br>"
                "The following is what would be sent:"
                "<br>"
                f"""
<pre>
To:      {', '.join(to_addresses)}
From:    {from_address}
Subject: {subject}
--
{content}
</pre>"""
            )
        )
