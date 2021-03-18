from typing import List
from typing import Tuple

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.transaction import atomic


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("password", type=str)

    @atomic
    def handle(self, *args, **kwargs):
        """
        Create all users with the same password
        """
        self.password = kwargs["password"]
        self._create_staff_users(
            [
                ("sophy@owlimmigration.com", "Sophy", "King"),
                ("dandavison7@gmail.com", "Dan", "Davison"),
            ]
        )
        self._create_users_and_groups(
            "Corporate Users",
            [
                ("corporate-user-alice@gmd.com", "Alice", "CorporateUser"),
                ("corporate-user-benoit@gmd.com", "Benoit", "CorporateUser"),
            ],
        )
        self._create_users_and_groups(
            "Service Providers",
            [
                ("service-provider-carlos@gmd.com", "Carlos", "ServiceProvider"),
                ("service-provider-dimitri@gmd.com", "Dimitri", "ServiceProvider"),
            ],
        )

    def _create_staff_users(self, user_data: List[Tuple[str, str, str]]) -> None:
        for (email, first_name, last_name) in user_data:
            User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=self.password,
                is_staff=True,
            )

    def _create_users_and_groups(
        self, group_name: str, user_data: List[Tuple[str, str, str]]
    ) -> None:
        group = Group.objects.create(name=group_name)

        for (email, first_name, last_name) in user_data:
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=self.password,
            )
            user.groups.add(group)
