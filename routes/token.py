from flask import Blueprint, request

from utils.function_jwt import write_token

routes_token = Blueprint("routes_token", __name__)


@routes_token.route("/crearToken", methods=['POST'])
def create_token():
    data = request.get_json()
    return write_token(data=request.get_json()), 200
