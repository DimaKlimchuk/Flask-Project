from flask_sqlalchemy import SQLAlchemy
from . import app 
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=0.0)

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Expense(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    amount = db.Column(db.Float, nullable=False)

with app.app_context():
    db.init_app(app)
    db.create_all()
