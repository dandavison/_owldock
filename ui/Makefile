SHELL = bash -u
WITH_NODE_ENV=env $$(xargs < .env)
WITH_SERVER_ENV=env $$(xargs < .env.server)

static-analysis: lint type-check

lint: backend-create-typescript-interfaces
	npm run lint

type-check: backend-create-typescript-interfaces
	npm run type-check

test: backend-create-typescript-interfaces
	npm run test

test-live: backend-create-typescript-interfaces
	$(WITH_NODE_ENV) npx cypress open

build: backend-create-typescript-interfaces
	$(WITH_SERVER_ENV) npm run build

serve: backend-create-typescript-interfaces
	$(WITH_NODE_ENV) npm run serve

watch:
	fswatch -or src | xargs -n1 -I{} make build

vscode:
	code .

backend-create-typescript-interfaces:
	cd ../backend && make create-typescript-interfaces
