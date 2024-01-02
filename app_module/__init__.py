from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://my_db_4ign_user:yFCOufRWPj4vzVmaqJnteyQKBlj5N3Ls@dpg-cm8rhfed3nmc73cjo1r0-a/my_db_4ign")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = '336994360382009747173282000561199201483'

db = SQLAlchemy(app)

migrate = Migrate(app, db, command='migrate')

jwt = JWTManager(app)

# Обробники помилок для JWT

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
   return (
       jsonify({"message": "The token has expired.", "error": "token_expired"}),
       401,
   )

@jwt.invalid_token_loader
def invalid_token_callback(error):
   return (
       jsonify(
           {"message": "Signature verification failed.", "error": "invalid_token"}
       ),
       401,
   )

@jwt.unauthorized_loader
def missing_token_callback(error):
   return (
       jsonify(
           {
               "description": "Request does not contain an access token.",
               "error": "authorization_required",
           }
       ),
       401,
   )

import app_module.models  
import app_module.views

with app.app_context():
    db.create_all()

  
