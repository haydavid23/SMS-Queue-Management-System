from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact:

    def __init__(self, name, number):
        self.name = name
        self.number = number




class Queeue:

    def __init__(self):
        self._queeue = []
        self._mode = "FIFO"

    def enqueue(self, name):
        self._queeue.append(name)

    def dequeue(self):
        self._queeue.pop(0)

    def __repr__(self):
       return (self._queeue)

"""
Q = Queeue()
Q.enqueue("David")
Q.enqueue("Hello")
Q.enqueue("Bye")
Q.dequeue("David")
print(repr(Q._queeue))

"""




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

