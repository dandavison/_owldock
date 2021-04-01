MANAGE=.venv/bin/python manage.py

static-analysis: lint type-check

lint:
	pylint --rcfile=.pylintrc app owldock

type-check: type-check-mypy

test:
	.venv/bin/pytest

test-all: lint type-check test

serve:
	$(MANAGE) runserver --settings=owldock.settings.dev 0.0.0.0:8000

type-check-mypy:
	.venv/bin/mypy .

type-check-pyright:
	pyright --venv-path . app owldock

repl-python:
	$(MANAGE) shell_plus

create-fake-data:
	$(MANAGE) create_fake_data

create-typescript-interfaces:
	$(MANAGE) create_typescript_interfaces ../ui/src/api-types.ts > /dev/null

recreate-db:
	rm -f db.sqlite3 \
	&& rm -rf app/migrations/* \
	&& ./manage.py makemigrations app \
	&& ./manage.py migrate \
	&& ./manage.py create_fake_data $$OWLDOCK_DEV_PASSWORD

db-graph:
	$(MANAGE) graph_models app --no-inheritance --exclude-models '*BaseModel' --output /tmp/db.svg

vscode:
	code .
