from flask import jsonify, request
from datetime import datetime
from app_module import app 
from marshmallow import ValidationError
from .schemas import UserSchema, CategorySchema, RecordSchema
from .models import User, Category, Record

user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()



@app.route('/')
def home():
    return 'Hello, this is the home page!'


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    status = "ok"
    return jsonify({"status": status})



@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    
    new_user = User(name=data['name'], balance=0.0)
    new_user.save()

      
    response_data = {'id': str(new_user.id), 'name': new_user.name, 'balance': new_user.balance}
    return jsonify(response_data), 201


@app.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.objects(id=user_id).first()

    if user:
        user_data = {'id': str(user.id), 'name': user.name, 'balance': user.balance}
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/user/<string:user_id>/update_balance', methods=['POST'])
def update_balance(user_id):
    user = User.objects(id=user_id).first()

    if user:
        try:
            data = request.get_json(force=True)
            amount = data.get('amount', 0.0)
            user.balance += amount
            user.save()
            return jsonify({'message': f'Balance updated successfully. New balance: {user.balance}'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.objects(id=user_id).first()

    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['GET'])
def get_users():
    users = User.objects()

    users_data = [{'id': str(user.id), 'name': user.name, 'balance': user.balance} for user in users]
    return jsonify(users_data)


@app.route('/category', methods=['POST'])
def create_category():
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    new_category = Category(name=data['name'])
    new_category.save()

    response_data = {'id': str(new_category.id), 'name': new_category.name}
    return jsonify(response_data), 201


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.objects()

    categories_data = [{'id': str(category.id), 'name': category.name} for category in categories]
    return jsonify(categories_data)


@app.route('/category/<string:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.objects(id=category_id).first()

    if category:
        category.delete()
        return jsonify({'message': 'Category deleted successfully'})
    else:
        return jsonify({'error': 'Category not found'}), 404


@app.route('/record', methods=['POST'])
def create_expense():
    try:
        data = record_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    user_id = data.get('user_id')
    amount = data.get('amount')

    user = User.objects(id=user_id).first()

    if user:
        if user.balance >= amount:
            expense = Record(
                user_id=user_id,
                category_id=data.get('category_id'),
                timestamp=datetime.utcnow(),
                amount=amount
            )
            expense.save()

            user.balance -= amount
            user.save()

            return jsonify({'message': 'Expense recorded successfully', 'user_balance': user.balance}), 201
        else:
            return jsonify({'error': 'Insufficient funds'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404



@app.route('/record/<string:record_id>', methods=['GET'])
def get_expense(record_id):
    expense = Record.objects(id=record_id).first()

    if expense:
        expense_data = {
            'id': str(expense.id),
            'user_id': str(expense.user_id.id),
            'category_id': str(expense.category_id.id),
            'timestamp': expense.timestamp.isoformat(),
            'amount': expense.amount
        }
        return jsonify(expense_data)
    else:
        return jsonify({'error': 'Record not found'}), 404


@app.route('/record/<string:record_id>', methods=['DELETE'])
def delete_expense(record_id):
    expense = Record.objects(id=record_id).first()

    if expense:
        expense.delete()
        return jsonify({'message': 'Record deleted successfully'})
    else:
        return jsonify({'error': 'Record not found'}), 404


@app.route('/record', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({'error': 'Please provide user_id and/or category_id as parameters'}), 400

    filters = {}
    if user_id:
        try:
            user_id = int(user_id)
            filters['user_id'] = user_id
        except ValueError:
            return jsonify({'error': 'Invalid user_id parameter'}), 400
    if category_id:
        try:
            category_id = int(category_id)
            filters['category_id'] = category_id
        except ValueError:
            return jsonify({'error': 'Invalid category_id parameter'}), 400

    expenses = Record.objects(**filters)

    expenses_data = [
        {
            'id': str(expense.id),
            'user_id': str(expense.user_id.id),
            'category_id': str(expense.category_id.id),
            'timestamp': expense.timestamp.isoformat(),
            'amount': expense.amount
        }
        for expense in expenses
    ]
    return jsonify(expenses_data)













