PSQL=psql -v ON_ERROR_STOP=1
SHELL = bash -u
WITH_NODE_ENV=env $$(xargs < .env)
WITH_SERVER_ENV=env $$(xargs < .env.server)

static-analysis: backend-static-analysis ui-static-analysis

test: backend-test ui-test

serve: ui-build backend-serve

clean:
	rm -fr ui/dist

vscode: backend-vscode ui-vscode

################################################################
# Backend

backend-static-analysis: backend-lint backend-type-check

backend-lint:
	cd backend && pylint --rcfile=.pylintrc app gmd

backend-type-check:
	cd backend && .venv/bin/mypy --check-untyped-defs .

backend-test:
	cd backend && .venv/bin/pytest

backend-serve:
	cd backend && ./manage.py runserver

backend-create-fake_data:
	cd backend && .venv/bin/python manage.py create_fake_data

backend-create-typescript-interfaces:
	cd backend && .venv/bin/python manage.py create_typescript_interfaces ../ui/src/api-types.ts > /dev/null

backend-destroy-db:
	cd backend \
	&& rm -f db.sqlite3 \
	&& rm -rf app/migrations/* \
	&& ./manage.py makemigrations app \
	&& ./manage.py migrate \
	&& ./manage.py create_users_and_groups $$GMD_DEV_PASSWORD \
	&& ./manage.py create_fake_data

backend-vscode:
	cd backend && code .

################################################################
# ui

ui-static-analysis: ui-lint ui-type-check

ui-lint: backend-create-typescript-interfaces
	cd ui && npm run lint

ui-type-check: backend-create-typescript-interfaces
	cd ui && npm run type-check

ui-test: backend-create-typescript-interfaces
	cd ui && npm run test

ui-test-live: backend-create-typescript-interfaces
	cd ui && $(WITH_NODE_ENV) npx cypress open

ui-build: backend-create-typescript-interfaces
	cd ui && $(WITH_SERVER_ENV) npm run build

ui-serve: backend-create-typescript-interfaces
	cd ui && npm run serve

ui-vscode:
	cd ui && code .
