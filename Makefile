PSQL=psql -v ON_ERROR_STOP=1
SHELL = bash -u
WITH_NODE_ENV=env $$(xargs < .env)
WITH_SERVER_ENV=env $$(xargs < .env.server)

serve: ui-build backend-serve

ui-build:
	cd ui && $(WITH_SERVER_ENV) npm run build

ui-serve:
	cd ui && npm run serve

backend-serve:
	cd backend && ./manage.py runserver

backend-type-check:
	cd backend && .venv/bin/mypy --check-untyped-defs .

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
	&& ./manage.py create_users_and_groups $$GMD_DEV_PASSWORD

test: test-ui test-backend

ui-test:
	cd ui && npm test

ui-test-live:
	cd ui && $(WITH_NODE_ENV) npx cypress open

clean:
	rm -fr ui/dist
