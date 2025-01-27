local/install:
	python -m venv ./venv && \
	. ./venv/bin/activate && \
	poetry install

local/server: local/install
	. ./venv/bin/activate && \
	poetry run python manage.py runserver

local/db:
	docker-compose up -d

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

code/format:
	poetry run isort .
	poetry run black .
