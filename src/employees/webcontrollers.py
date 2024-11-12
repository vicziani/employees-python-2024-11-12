from flask import Blueprint, current_app, flash, jsonify, make_response, redirect, render_template, request, url_for
from wtforms import Form, StringField, validators
from . import repo

employeesweb = Blueprint('employeesweb', __name__, template_folder='templates')


class EmployeeForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])


@employeesweb.route("/", methods=["GET"])
def list_employees():
    return render_template("employees.html", employees=repo.find_all(), form=EmployeeForm())


@employeesweb.route("/", methods=["POST"])
def save_employee():
    form = EmployeeForm(request.form)
    # models.save({"name": request.form.get("name")})
    if form.validate():
        repo.save({"name": form.name.data})
        flash("Employee has been created")
        current_app.logger.info(f"Employee has been created: {form.name.data}")
        return redirect(url_for("employeesweb.list_employees"))
    current_app.logger.error(f"Errors: {form._fields.get('name').errors}")
    
    return render_template("employees.html", employees=repo.find_all(), form=form)
