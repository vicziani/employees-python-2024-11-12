import logging
import os

from flask import Flask

from . import repo
from .restcontrollers import employeesrest
from .webcontrollers import employeesweb

app = Flask(__name__)

DEFAULT_DATABASE_HOST = "localhost"
DATABASE_HOST = os.getenv("DATABASE_HOST", DEFAULT_DATABASE_HOST)
app.logger.info("Database HOST: %s", DATABASE_HOST)
app.config["DATABASE_HOST"] = DATABASE_HOST

DEFAULT_DATABASE_USER = "employees"
DATABASE_USER = os.getenv("DATABASE_USER", DEFAULT_DATABASE_USER)
app.config["DATABASE_USER"] = DATABASE_USER

DEFAULT_DATABASE_PASSWORD = "employees"  # nosec - default password
DATABASE_USER = os.getenv("DATABASE_PASSWORD", DEFAULT_DATABASE_PASSWORD)
app.config["DATABASE_PASSWORD"] = DEFAULT_DATABASE_PASSWORD

# RuntimeError: The session is unavailable because no secret key was set.
# Set the secret_key on the application to something unique and secret.
# sessionkezelés miatt
DEFAULT_SECRET_KEY = "employees"  # nosec - default value
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
app.config["SECRET_KEY"] = SECRET_KEY

app.logger.setLevel(logging.INFO)

app.register_blueprint(employeesweb)
app.register_blueprint(employeesrest)


@app.before_request
def init():
    repo.init()
