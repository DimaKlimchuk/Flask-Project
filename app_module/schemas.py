from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    timestamp = fields.DateTime(dump_only=True)
    amount = fields.Float(required=True)



