from flask import Blueprint, request, jsonify, session

from utils.authentication import *
from utils.function_jwt import validate_token
from functools import wraps

routes_user_auth = Blueprint("routes_user_auth", __name__)


def verify_token_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.get_json().get('admin'):
            token = request.headers.get('Authorization', '').split(" ")[1]
            response = validate_token(token)
            # Aquí puedes realizar acciones adicionales con la respuesta si es necesario
            # ...
        return func(*args, **kwargs)

    return wrapper


@routes_user_auth.route("/register", methods=['POST'])
# @verify_token_middleware
def add_cliente():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        email = info_result['email']
        password = info_result['password']
        createUser(email, password)
        return jsonify({"result": "usuario creado exitosamente"}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to create user'}), 500


@routes_user_auth.route("/login", methods=['POST'])
def login_user():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        email = info_result['email']
        password = info_result['password']
        loginUser(email, password)
        return jsonify({"result": "usuario logueado"}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to login'}), 500
