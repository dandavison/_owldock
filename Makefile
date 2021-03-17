PSQL=psql -v ON_ERROR_STOP=1
WITH_ENV_DEV=env $$(xargs < .env)
WITH_ENV_PROD=env $$(xargs < .env.prod)
SHELL = bash -u

build-ui:
	cd ui && $(WITH_ENV_PROD) npm run build

serve-ui:
	cd ui && npm run serve

serve-backend:
	$(WITH_ENV_DEV) cd backend && ./manage.py runserver

serve-backend-and-ui: build-ui serve-backend

type-check-backend:
	cd backend && .venv/bin/mypy --check-untyped-defs .

create_typescript_interfaces:
	cd backend && .venv/bin/python manage.py create_typescript_interfaces ../ui/src/api-types.ts > /dev/null

test: test-ui test-backend

test-ui:
	cd ui && npm test

test-ui-live:
	cd ui && $(WITH_ENV_DEV) npx cypress open

clean:
	rm -fr ui/dist
