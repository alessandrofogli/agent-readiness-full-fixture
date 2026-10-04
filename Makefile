.PHONY: setup test lint format typecheck drift-check flags-audit up down migrate rollback profile

setup:
	uv sync

test:
	uv run pytest -q

lint:
	uv run ruff check .
	uv run lint-imports

format:
	uv run ruff format .

typecheck:
	uv run mypy packages/api/src packages/worker/src

drift-check:
	uv run python scripts/check_version_drift.py

flags-audit:
	uv run python scripts/check_flags.py

up:
	docker compose up -d postgres redis pyroscope

down:
	docker compose down

migrate:
	uv run alembic -c packages/api/alembic.ini upgrade head

rollback:
	./scripts/rollback.sh

profile:
	./scripts/profile.sh
