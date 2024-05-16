from flask import jsonify, Flask
from flask_cors import CORS

from routes.Auth import routes_user_auth
from routes.Scrapers import routes_scrap
from utils.FirebaseService import FirebaseService

app = Flask(__name__)

firebase_service = FirebaseService()
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True,
            headers=['Authorization'],
            expose_headers='Authorization')


app.register_blueprint(routes_user_auth)
app.register_blueprint(routes_scrap)


@app.route("/", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running ..."
    return jsonify(json)


if __name__ == '__main__':
    app.run(port=5000)
