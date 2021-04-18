#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py migrate --database client
pip install django-seed==0.2.2 \
    && python manage.py create_fake_world \
    && pip uninstall -y django-seed
