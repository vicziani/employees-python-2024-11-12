"""
.. include:: ../../docs/src/repo.md
"""

import psycopg
from flask import current_app


def sql(funct):
    def wrap_function(*args, **kwargs):
        host = current_app.config.get("DATABASE_HOST")
        user = current_app.config.get("DATABASE_USER")
        password = current_app.config.get("DATABASE_PASSWORD")
        # https://github.com/pylint-dev/pylint/issues/5273
        # pylint: disable=E1129
        with psycopg.connect(
            user=user,
            password=password,
            host=host,
            dbname="employees",
        ) as conn:
            kwargs["conn"] = conn
            return funct(*args, **kwargs)

    return wrap_function


@sql
def init(conn=None):
    with current_app.app_context():
        with conn.cursor() as cursor:
            cursor.execute(
                """create table if not exists employees
                    (id serial not null primary key, emp_name varchar(255))"""
            )


@sql
def find_all(conn=None):
    with conn.cursor() as cursor:
        cursor.execute("select id, emp_name from employees")
        employees = []
        for emp_id, name in cursor:
            employees.append({"id": emp_id, "name": name})
        return employees


@sql
def save(command, conn=None):
    """Save an employee"""
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into employees(emp_name) values (%s) returning id",
            (command["name"],),
        )
        conn.commit()
        emp_id = cursor.fetchone()[0]
        return {"id": emp_id, "name": command["name"]}


@sql
def delete_all(conn=None):
    with conn.cursor() as cursor:
        cursor.execute("delete from employees")
        conn.commit()
