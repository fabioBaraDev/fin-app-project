local/install:
	python -m venv ./venv && \
	. source venv/bin/activate && \
	poetry install

local/enviroment: local/db local/install migrate local/server

local/server:
	. ./venv/bin/activate && \
	poetry run python manage.py runserver

docker/run:
	docker-compose up -d

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

code/format:
	poetry run isort .
	poetry run black .

tests/unit:
	poetry run python run_test.py

docker/local/enviroment: docker/run
	docker-compose exec web python manage.py migrate

