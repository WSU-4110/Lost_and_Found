from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
#app.template_folder = app.config['TEMPLATE_FOLDER']
db = SQLAlchemy(app)


from app import routes, models
