from flask import Blueprint, jsonify, request

from . import repo

employeesrest = Blueprint("employees", __name__, template_folder="templates")


@employeesrest.route("/info")
def info() -> int:
    x = 0
    return jsonify({"status": "on"})


@employeesrest.route("/api/employees", methods=["GET"])
def find_all():
    return jsonify(repo.find_all())


@employeesrest.route("/api/employees", methods=["POST"])
def save():
    return repo.save(request.json), 201
