SHELL = bash -u

static-analysis:
	cd backend && make static-analysis
	cd ui && make static-analysis

test:
	cd backend && make test
	cd ui && make test

serve:
	cd ui && make build
	cd backend && make serve

clean:
	rm -fr ui/dist

vscode:
	cd backend && make vscode
	cd ui && make vscode
