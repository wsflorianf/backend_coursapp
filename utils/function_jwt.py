import base64

from flask import jsonify, json
from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta

from utils.encrypter import encrypt_dict


def expire_date(day: int):
    now = datetime.now()
    new_date = now + timedelta(days=day)
    return new_date


def write_token(data: dict):
    key = "NwKyZF848xFHInNmjQfY4U4uKTNGhK2ABqgHvolGhuA="
    encryptDict = encrypt_dict(data, key)
    token = encode(payload={**encryptDict, "exp": expire_date(1)}, key=key, algorithm="HS256")
    return verifyEncode(token)


def verifyEncode(string):
    try:
        encoded = string.encode('utf-8')
        return encoded
    except AttributeError:
        return string


def validate_token(token, output=False):
    try:
        if output:
            response = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
            return response
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response


def get_data(token):
    key = "NwKyZF848xFHInNmjQfY4U4uKTNGhK2ABqgHvolGhuA="
    return decode(token, key=key, algorithms=["HS256"])
