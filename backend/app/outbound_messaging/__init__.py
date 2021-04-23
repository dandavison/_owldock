from dataclasses import dataclass
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
        [case] = {s.case for s in self.case_steps}
        client_contact_user = case.client_contact.user

        to_addresses = [self.provider_contact.user.email]
        from_address = "owl@owldock.com"
        subject = "Your services have been requested"
        content = f"""\
Dear {self.provider_contact.provider.name} team,

{client_contact_user.first_name} {client_contact_user.last_name}
(case.client_contact.client.name)
has selected you to assist with a service!

Please log in to accept this work and learn the details

https://owldock.com/portal/case/{case.uuid}
"""
        send_mail(
            subject,
            content,
            from_address,
            to_addresses,
            fail_silently=False,
        )
        add_message(
            (
                "Owldock does not actually send notifications yet.<br>"
                "Here is the email that would be sent:"
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
