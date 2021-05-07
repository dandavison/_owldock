import os

from django.contrib.auth import get_user_model


def create_superusers() -> None:
    print("Creating superusers")
    for (email, first_name, last_name) in [
        ("dandavison7@gmail.com", "Dan", "Davison"),
        ("maria.kouri@corporaterelocations.gr", "Maria", "Kouri"),
        ("sophy@owlimmigration.com", "Sophy", "King"),
    ]:
        get_user_model().objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=os.environ["OWLDOCK_DEV_PASSWORD"],
            is_staff=True,
            is_superuser=True,
        )
