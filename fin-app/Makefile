local/install:
	python -m venv ./venv && \
	. source venv/bin/activate && \
	poetry install

local/enviroment: local/db local/install migrate local/server

local/server:
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

tests/unit:
	poetry run pytest

