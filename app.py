from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yuliya_database.db'  # SQLite database
db = SQLAlchemy(app)

# Define the Person model (as previously defined)
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    microblogs = db.relationship('Microblog', backref='author', lazy=True)
    sender_chats = db.relationship('Chat', foreign_keys='Chat.sender_id', backref='sender', lazy='dynamic')
    receiver_chats = db.relationship('Chat', foreign_keys='Chat.receiver_id', backref='receiver', lazy='dynamic')

# Define the Post model (as previously defined)
class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    itemType = db.Column(db.String(80), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120))
    status = db.Column(db.String(20), nullable=False)
    dateResolved = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

# Define the Microblog model (as previously defined)
class Microblog(db.Model):
    blogID = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

# Define the Conversation model
class Conversation(db.Model):
    conversation_id = db.Column(db.String(40), primary_key=True)
    participants = db.relationship('Person', secondary='conversation_participants', backref='conversations')

class ConversationParticipants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    conversation_id = db.Column(db.String(40), db.ForeignKey('conversation.conversation_id'))

# Define the Chat model
class Chat(db.Model):
    chatID = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    conversation_id = db.Column(db.String(40), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
