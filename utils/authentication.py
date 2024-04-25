import pyrebase
from flask import jsonify

class FirebaseService:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(FirebaseService, cls).__new__(cls)
            config = {
                "apiKey": "AIzaSyDcaYS9Uv4jmrbMKtNVthwZo5KJRnuQIww",
                'authDomain': "cursapp-5a097.firebaseapp.com",
                'projectId': "cursapp-5a097",
                'storageBucket': "cursapp-5a097.appspot.com",
                'messagingSenderId': "1076030716091",
                'appId': "1:1076030716091:web:2b981bfd415e6a62ebd19e",
                'databaseURL': ""
            }
            firebase = pyrebase.initialize_app(config)
            cls.instance.auth = firebase.auth()
        return cls.instance


def createUser(email, password):
    firebase_service = FirebaseService()
    auth = firebase_service.auth
    auth.create_user_with_email_and_password(email, password)


def loginUser(email, password):
    firebase_service = FirebaseService()
    auth = firebase_service.auth
    auth.sign_in_with_email_and_password(email, password)

