from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test-pwd@db/my_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

migrate = Migrate(app, db, command='migrate')
import app_module.models  
import app_module.views

with app.app_context():
    db.create_all()





  
