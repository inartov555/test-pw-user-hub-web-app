setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e . && playwright install --with-deps

run:
	pytest -n auto -q

docker:
	docker compose run --rm tests
