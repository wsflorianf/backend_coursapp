import datetime

import firebase_admin
from firebase_admin import credentials, firestore, auth


class FirebaseService:
    instance = None
    db = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(FirebaseService, cls).__new__(cls)
            cred = credentials.Certificate('./cursapp-5a097-firebase-adminsdk-yizdk-ee3a456a21.json')
            firebase_admin.initialize_app(cred)
            cls.db = firestore.client()
        return cls.instance

    @staticmethod
    def create_user(email, password):
        try:
            user = auth.create_user(email=email, password=password)
            custom_token = auth.create_custom_token(user.uid)
            if isinstance(custom_token, bytes):
                custom_token = custom_token.decode('utf-8')
            FirebaseService.log_event('create_user', user_id=user.uid, email=email)
            return custom_token
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    @staticmethod
    def get_user(email):
        try:
            user = auth.get_user_by_email(email)
            FirebaseService.log_event('get_user', user_id=user.uid, email=email)
            return user
        except Exception as e:
            raise Exception(f"Error fetching user: {str(e)}")

    @staticmethod
    def create_session_cookie(id_token, expires_in):
        try:
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            decoded_token = auth.verify_id_token(id_token)
            FirebaseService.log_event('create_session_cookie', user_id=decoded_token['uid'])  # Registrar evento
            return session_cookie
        except Exception as e:
            raise Exception(f"Error creating session cookie: {str(e)}")

    @staticmethod
    def log_event(action, user_id=None, email=None, extra_info=None):
        doc_ref = FirebaseService.db.collection('user_logs').document()
        log_data = {
            'action': action,
            'timestamp': firestore.firestore.SERVER_TIMESTAMP
        }
        if user_id:
            log_data['user_id'] = user_id
        if email:
            log_data['email'] = email
        if extra_info:
            log_data.update(extra_info)
        doc_ref.set(log_data)

    @staticmethod
    def log_click(click_data):
        try:
            user_id = click_data.pop('user_id')
            user = auth.get_user(user_id)
            email = user.email
            current_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            user_doc_ref = FirebaseService.db.collection('user_clicks').document(user_id)
            all_clicks_ref = FirebaseService.db.collection('user_clicks').document("all_clicks")
            click_data['timestamp'] = datetime.datetime.utcnow()

            user_doc = user_doc_ref.get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                daily_clicks = user_data.get(current_date, {}).get('clicks', [])
                if not isinstance(daily_clicks, list):
                    daily_clicks = []
            else:
                daily_clicks = []

            click_data_with_user_id = {**click_data, 'user_id': user_id}
            daily_clicks.append(click_data)
            user_doc_ref.set({
                current_date: {'clicks': daily_clicks},
                'email': email
            }, merge=True)

            all_doc = all_clicks_ref.get()
            if all_doc.exists:
                all_data = all_doc.to_dict()
                all_daily_clicks = all_data.get(current_date, {}).get('clicks', [])
                if not isinstance(all_daily_clicks, list):
                    all_daily_clicks = []
            else:
                all_daily_clicks = []

            all_daily_clicks.append(click_data_with_user_id)
            all_clicks_ref.set({
                current_date: {'clicks': all_daily_clicks}
            }, merge=True)

        except Exception as e:
            raise Exception(f"Error logging click: {str(e)}")
