from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""
class Queeue:

    def __init__(self, queeue):
        self._queeue = []
        self._mode = "FIFO"

    def enqueue(self, item):
            self._queeue.append(self, body)

    def dequeue(self, item):
        self._queeue.pop(self, i)
    def get_queue(self):
        queeue.copy()

    def size(self):
        return len(self._queue)

queeue = Queeue (body)

#if request == POST
queeue.enqueue()

#if request == GET
queeue.dequeue()

"""
print("hello")




class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }