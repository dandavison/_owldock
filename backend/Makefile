static-analysis: lint type-check

lint:
	pylint --rcfile=.pylintrc app gmd

type-check:
	.venv/bin/mypy --check-untyped-defs .

test:
	.venv/bin/pytest

serve:
	./manage.py runserver

create-fake_data:
	.venv/bin/python manage.py create_fake_data

create-typescript-interfaces:
	.venv/bin/python manage.py create_typescript_interfaces ../ui/src/api-types.ts > /dev/null

destroy-db:
	rm -f db.sqlite3 \
	&& rm -rf app/migrations/* \
	&& ./manage.py makemigrations app \
	&& ./manage.py migrate \
	&& ./manage.py create_users_and_groups $$GMD_DEV_PASSWORD \
	&& ./manage.py create_fake_data

vscode:
	code .
