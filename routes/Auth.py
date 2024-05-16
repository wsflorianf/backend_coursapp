import datetime

from flask import Blueprint, request, jsonify, session

from utils.FirebaseService import *
from flask import g
from functools import wraps
from firebase_admin.exceptions import FirebaseError

routes_user_auth = Blueprint("routes_user_auth", __name__)


def verify_token_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_cookie = request.cookies.get('session')
        if not session_cookie:
            return jsonify({"error": "No session cookie found"}), 401
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
            g.decoded_claims = decoded_claims
        except FirebaseError as e:
            return jsonify({"error": "Invalid or expired session cookie", "message": str(e)}), 403
        return func(*args, **kwargs)

    return wrapper


@routes_user_auth.route("/register", methods=['POST'])
# @verify_token_middleware
def create_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        custom_token = FirebaseService.create_user(email, password)
        return jsonify({'customToken': custom_token}), 200
    except Exception as e:
        return jsonify({"error": "Failed to create user", "message": str(e)}), 500


@routes_user_auth.route('/session_login', methods=['POST'])
def session_login():
    id_token = request.json.get('idToken')
    expires_in = 2 * 60 * 60
    try:
        session_cookie = FirebaseService.create_session_cookie(id_token, expires_in=expires_in)
        response = jsonify({"status": "success"})
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        response = response
        response.set_cookie('session', session_cookie, expires=expires, httponly=True, secure=True)
        return response
    except Exception as e:
        return jsonify({"error": "Failed to create a session cookie", "message": str(e)}), 401


@routes_user_auth.route('/register_click', methods=['POST'])
@verify_token_middleware
def register_click():
    try:
        data = request.get_json()
        user_id = g.decoded_claims['uid'] if g.decoded_claims else None
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        click_data = {
            'user_id': user_id,
            'page': data.get('page'),
            'element_id': data.get('element_id', ""),
            'extra_info': data.get('extra_info', {})
        }
        FirebaseService.log_click(click_data)
        return jsonify({"status": "click registered"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to register click", "message": str(e)}), 500

# @routes_user_auth.route("/login", methods=['POST'])
# def login_user():
#     try:
#         # Obtener los parámetros del cuerpo de la solicitud
#         info_result = request.get_json()
#         email = info_result['email']
#         password = info_result['password']
#         loginUser(email, password)
#         return jsonify({"result": "usuario logueado"}), 200
#     except Exception as e:
#         return jsonify({'error': 'Failed to login'}), 500
