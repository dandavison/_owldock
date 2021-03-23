static-analysis: lint type-check

lint:
	pylint --rcfile=.pylintrc app gmd

type-check: type-check-mypy

test:
	.venv/bin/pytest

serve:
	./manage.py runserver

type-check-mypy:
	.venv/bin/mypy .

type-check-pyright:
	pyright --venv-path . app gmd

repl-python:
	./manage.py shell_plus

create-fake_data:
	.venv/bin/python manage.py create_fake_data

create-typescript-interfaces:
	.venv/bin/python manage.py create_typescript_interfaces ../ui/src/api-types.ts > /dev/null

destroy-db:
	rm -f db.sqlite3 \
	&& rm -rf app/migrations/* \
	&& ./manage.py makemigrations app \
	&& ./manage.py migrate \
	&& ./manage.py create_fake_data $$GMD_DEV_PASSWORD

vscode:
	code .
