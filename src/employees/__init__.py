from flask import Flask
from .webcontrollers import employeesweb
from .restcontrollers import employeesrest
from . import repo
import os
import logging

app = Flask(__name__)

DEFAULT_DATABASE_HOST = 'localhost'
DATABASE_HOST = os.environ.get("DATABASE_HOST", DEFAULT_DATABASE_HOST)
app.logger.info(f"Database HOST: {DATABASE_HOST}")
app.config['DATABASE_HOST'] = DATABASE_HOST

# RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
# sessionkezelés miatt
app.config['SECRET_KEY'] = "employees"

app.logger.setLevel(logging.INFO)

app.register_blueprint(employeesweb)
app.register_blueprint(employeesrest)

@app.before_request
def init():
    repo.init()