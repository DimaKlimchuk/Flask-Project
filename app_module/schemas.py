from marshmallow import Schema, fields
from datetime import datetime


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    balance = fields.Float(dump_only=True)


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Str(required=True)
    category_id = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    amount = fields.Float(required=True)


