import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Queeue

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
Q1 = Queeue()
# print(repr(Q1._queeue))

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():

    return generate_sitemap(app)

@app.route('/person', methods=['POST', 'GET', "DELETE"])
def handle_person():

    """
    Create person and retrieve all persons
    """
     # DELETE request
    if request.method == 'DELETE':
        Q1.dequeue()
        print(repr(Q1._queeue))

        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        db.session.commit()

    # POST request

    if request.method == 'POST':
        body = request.get_json()


        Q1.enqueue(body["guest"])
        print(repr(Q1._queeue))

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        user1 = Person(username=body['username'], email=body['email'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200


    # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404


@app.route('/person/<int:person_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_person(person_id):
    """
    Single person
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if "username" in body:
            user1.username = body["username"]
        if "email" in body:
            user1.email = body["email"]
        db.session.commit()

        return jsonify(user1.serialize()), 200

    # GET request
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)