# Build the final image
FROM ubuntu:latest

WORKDIR /srv

RUN apt update && apt install python3-pip netcat libpq-dev -y
RUN pip install poetry==1.2

COPY . .
RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "/srv/docker/entrypoint.sh"]
CMD ["gunicorn", "werubin.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "300"]