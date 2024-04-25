from flask import jsonify
from jwt import exceptions


def verifyExceptions(e: Exception):
    if isinstance(e, exceptions.DecodeError):
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    if isinstance(e, exceptions.ExpiredSignatureError):
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response
    return jsonify({'error': str(e)}), 500
