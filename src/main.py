import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import Person, Queeue  # db

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app)  # db)
# db.init_app(app)
CORS(app)
Q1 = Queeue()
# print(repr(Q1._queeue))

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():

    return generate_sitemap(app)

@app.route('/new', methods=['POST'])
def handle_person():

     # POST request to Add person to queeue.

    if request.method == 'POST':
        body = request.get_json()

        Q1.enqueue(body["guest"])
        print(repr(Q1._queeue))

    return "ok", 200

@app.route('/all', methods=['GET'])
def handle_get():

    # GET request - Returns everyone that is pending.
    if request.method == 'GET':

        return repr(Q1._queeue), 200




@app.route('/next', methods=['DELETE'])
def process_person():

    # Process Person and Deletes Person from Queeue

    if request.method == 'DELETE':
        Q1.dequeue()
        print(repr(Q1._queeue))

    return "ok", 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)