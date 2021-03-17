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
        password = kwargs["password"]
        sophy = "sophy@owlimmigration.com"
        dan = "dandavison7@gmail.com"

        staff_users = [sophy, dan]
        for email in staff_users:
            User.objects.create_user(
                username=email, email=email, password=password, is_staff=True
            )

        Group.objects.create(name="Corporate Users")
        Group.objects.create(name="Service Providers")

        User.objects.create_user(
            username="corporate-user@gmd.com", email=dan, password=password
        )
        User.objects.create_user(
            username="service-provider@gmd.com", email=dan, password=password
        )
