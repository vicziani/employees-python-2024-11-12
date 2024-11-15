FROM python:3.11.2-slim-bullseye

RUN apt-get -y update; apt-get -y install curl

WORKDIR /app
COPY dist/employees*.whl .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir employees*.whl

# ENTRYPOINT ["flask", "--app", "employees", "run", "--host", "0.0.0.0"]
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "employees:app"]