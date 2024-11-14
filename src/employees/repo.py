import psycopg
from flask import current_app


def sql(funct):
    def wrap_function(*args, **kwargs):
        host = current_app.config.get("DATABASE_HOST")
        with psycopg.connect(
            user="employees", password="employees", host=host, dbname="employees"
        ) as conn:
            kwargs["conn"] = conn
            return funct(*args, **kwargs)

    return wrap_function


@sql
def init(conn=None):
    with current_app.app_context():
        with conn.cursor() as cursor:
            cursor.execute(
                "create table if not exists employees (id serial not null primary key, emp_name varchar(255))"
            )


@sql
def find_all(conn=None):
    with conn.cursor() as cursor:
        cursor.execute("select id, emp_name from employees")
        employees = []
        for id, name in cursor:
            employees.append({"id": id, "name": name})
        return employees


@sql
def save(command, conn=None):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into employees(emp_name) values (%s) returning id",
            (command["name"],),
        )
        conn.commit()
        id = cursor.fetchone()[0]
        return {"id": id, "name": command["name"]}


@sql
def delete_all(conn=None):
    with conn.cursor() as cursor:
        cursor.execute("delete from employees")
        conn.commit()
