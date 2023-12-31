from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://my_db_4ign_user:yFCOufRWPj4vzVmaqJnteyQKBlj5N3Ls@dpg-cm8rhfed3nmc73cjo1r0-a/my_db_4ign'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

migrate = Migrate(app, db, command='migrate')
import app_module.models  
import app_module.views

with app.app_context():
    db.create_all()





  
