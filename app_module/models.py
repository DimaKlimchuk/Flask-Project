from mongoengine import Document, fields
from datetime import datetime

class User(Document):
    name = fields.StringField(required=True)
    balance = fields.FloatField(default=0.0)

class Category(Document):
    name = fields.StringField(required=True)

class Record(Document):
    user_id = fields.ReferenceField(User, required=True)
    category_id = fields.ReferenceField(Category, required=True)
    timestamp = fields.DateTimeField(default=datetime.utcnow, required=True)
    amount = fields.FloatField(required=True)
