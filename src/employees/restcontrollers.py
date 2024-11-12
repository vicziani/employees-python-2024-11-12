from flask import Blueprint, current_app, jsonify, make_response, request
from . import repo

employeesrest = Blueprint('employees', __name__, template_folder='templates')


@employeesrest.route("/info")
def info():
    return '{"status" = "on"}'


@employeesrest.route("/api/employees", methods=['GET'])
def find_all():
    # jsonify nélkül nem megy
    return jsonify(repo.find_all())


@employeesrest.route('/api/employees', methods=['POST'])
def save():
    return repo.save(request.json), 201
