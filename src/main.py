import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import Person, Queeue, Contact # db
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse

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
        #body = request.get_json()

        number = request.form['From']
        message_body = request.form['Body']
        C1 = Contact(message_body, number)



        Q1.enqueue(message_body, number)




    print(repr(Q1._queeue))

    resp = MessagingResponse()

    resp.message("Hello " + message_body + " you have been added."  " There are " + repr(len(Q1._queeue)-1) + " person in front of you.")

    return  str(resp)



@app.route('/all', methods=['GET'])
def handle_get():

    # GET request - Returns everyone that is pending.
    if request.method == 'GET':


        return jsonify(Q1._queeue), 200


@app.route('/process', methods=['GET'])
def process():


    account_sid = 'AC099f45babe1d5656b38554a3fae90cc2'
    auth_token = 'f0e9da1e9346cd9cd09cfdc00e30b53a'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='It is your Turn.',
        from_='+17868082401',
        to = Q1.numbers[0]
                          )

    print(message.sid)

    return repr(Q1._queeue[0])


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