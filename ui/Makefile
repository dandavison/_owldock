SHELL = bash -u
WITH_CYPRESS_DJANGO_ENV=env $$(xargs < .env.cypress-django)
WITH_NODE_ENV=env $$(xargs < .env)
WITH_SERVER_ENV=env $$(xargs < .env.server)

static-analysis: lint type-check

lint: backend-generate-typescript-interfaces
	npm run lint

type-check: backend-generate-typescript-interfaces
	npm run type-check

test:
	npx cypress run

test-live: backend-generate-typescript-interfaces
	$(WITH_CYPRESS_DJANGO_ENV) npx cypress open


build: backend-generate-typescript-interfaces
	$(WITH_SERVER_ENV) npm run build

build-watch: backend-generate-typescript-interfaces
	$(WITH_SERVER_ENV) npm run build-watch

serve: backend-generate-typescript-interfaces
	$(WITH_NODE_ENV) npm run serve

vscode:
	code .

backend-generate-typescript-interfaces:
	cd ../backend && make generate-typescript-interfaces
