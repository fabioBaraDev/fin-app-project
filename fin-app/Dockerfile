FROM python:3.12.7

WORKDIR /app


RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --without dev --no-root

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]