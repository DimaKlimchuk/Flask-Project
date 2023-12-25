from flask import jsonify, request
from datetime import datetime
from app_module import app
from .schemas import UserSchema, CategorySchema, ExpenseSchema


user_schema = UserSchema()
category_schema = CategorySchema()
expense_schema = ExpenseSchema()

users = [
    {'id': 1, 'name': 'John Doe'},
    {'id': 2, 'name': 'Jane Smith'},
]

categories = [
    {'id': 1, 'name': 'Food'},
    {'id': 2, 'name': 'Utilities'},
]

expenses = [
    {'id': 1, 'user_id': 1, 'category_id': 1, 'timestamp': '2023-01-01 12:00:00', 'amount': 20.0},
    {'id': 2, 'user_id': 2, 'category_id': 1, 'timestamp': '2023-01-02 14:30:00', 'amount': 15.0},
]

@app.route('/')
def home():
    return 'Hello, this is the home page!'

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        status = "ok"
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        if 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400

        user = {
            'id': len(users) + 1,
            'name': data['name']
        }
        users.append(user)
        result = user_schema.dump(user)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            result = user_schema.dump(user)
            return jsonify(result)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        global users
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            users = [u for u in users if u['id'] != user_id]
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        result = user_schema.dump(users, many=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/record', methods=['POST'])
def create_expense():
    try:
        data = request.get_json()
        errors = expense_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        required_fields = ['user_id', 'category_id', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Required fields: {", ".join(required_fields)}'}), 400

        expense = {
            'id': len(expenses) + 1,
            'user_id': int(data['user_id']),
            'category_id': int(data['category_id']),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': float(data['amount'])
        }
        expenses.append(expense)
        result = expense_schema.dump(expense)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        if not categories:
            return jsonify({'error': 'No categories available'}), 404

        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        global categories
        category = next((category for category in categories if category['id'] == category_id), None)
        if category:
            categories = [c for c in categories if c['id'] != category_id]
            return jsonify({'message': 'Category deleted successfully'})
        else:
            return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/record', methods=['POST'])
def create_expense():
    try:
        data = request.get_json()
        errors = expense_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        required_fields = ['user_id', 'category_id', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Required fields: {", ".join(required_fields)}'}), 400

        expense = {
            'id': len(expenses) + 1,
            'user_id': int(data['user_id']),
            'category_id': int(data['category_id']),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': float(data['amount'])
        }
        expenses.append(expense)
        result = expense_schema.dump(expense)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/record/<int:record_id>', methods=['GET'])
def get_expense(record_id):
    try:
        record = next((expense for expense in expenses if expense['id'] == record_id), None)
        if record:
            result = expense_schema.dump(record)
            return jsonify(result)
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_expense(record_id):
    try:
        global expenses
        record = next((expense for expense in expenses if expense['id'] == record_id), None)
        if record:
            expenses = [e for e in expenses if e['id'] != record_id]
            return jsonify({'message': 'Record deleted successfully'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/record', methods=['GET'])
def get_expenses():
    try:
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')

        if not user_id and not category_id:
            result = expense_schema.dump(expenses, many=True)
            return jsonify(result)

        filtered_expenses = expenses
        if user_id:
            filtered_expenses = [expense for expense in filtered_expenses if expense['user_id'] == int(user_id)]
        if category_id:
            filtered_expenses = [expense for expense in filtered_expenses if expense['category_id'] == int(category_id)]

        result = expense_schema.dump(filtered_expenses, many=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



