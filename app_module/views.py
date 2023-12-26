from flask import jsonify, request
from datetime import datetime
from app_module import app 
from .schemas import UserSchema, CategorySchema, RecordSchema

user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()



users = [
    {'id': 1, 'name': 'John Doe', 'balance': 0.0},
    {'id': 2, 'name': 'Jane Smith', 'balance': 0.0},
]

    
category = [
        {'id': 1, 'name': 'Food'},
        {'id': 2, 'name': 'Utilities'},
        
    ]

   
record = [
        {'id': 1, 'user_id': 1, 'category_id': 1, 'timestamp': '2023-01-01 12:00:00', 'amount': 20.0},
        {'id': 2, 'user_id': 2, 'category_id': 1, 'timestamp': '2023-01-02 14:30:00', 'amount': 15.0},
    ]


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

    user = {
        'id': len(users) + 1,
        'name': data['name'],
        'balance': 0.0,
    }
    users.append(user)
    return jsonify(user), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user_schema.dump(user))
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/user/<int:user_id>/update_balance', methods=['POST'])
def update_balance(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        try:
            data = user_schema.load(request.get_json(), partial=('name',))
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400

        amount = data.get('amount', 0.0)
        user['balance'] += amount
        return jsonify({'message': f'Balance updated successfully. New balance: {user["balance"]}'})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        users = [u for u in users if u['id'] != user_id]
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(user_schema.dump(users, many=True))


@app.route('/category', methods=['POST'])
def create_category():
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    category = {
        'id': len(categories) + 1,
        'name': data['name']
    }
    category.append(category)
    return jsonify(category), 201


@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(category_schema.dump(category, many=True))


@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    global categories
    category = next((category for category in categories if category['id'] == category_id), None)
    if category:
        categories = [c for c in categories if c['id'] != category_id]
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

    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        if user['balance'] >= amount:
            expense = {
                'id': len(expenses) + 1,
                'user_id': user_id,
                'category_id': data.get('category_id'),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'amount': amount
            }

            record.append(expense)
            user['balance'] -= amount

            return jsonify({'message': 'Expense recorded successfully', 'user_balance': user['balance']}), 201
        else:
            return jsonify({'error': 'Insufficient funds'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404



@app.route('/record/<int:record_id>', methods=['GET'])
def get_expense(record_id):
    one_record = next((e for e in record if e['id'] == record_id), None)
    if one_record:
        return jsonify(one_record)
    else:
        return jsonify({'error': 'Record not found'}), 404


@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_expense(record_id):
    global expenses
    expenses = [expense for expense in expenses if expense['id'] != record_id]
    return jsonify({'message': 'Record deleted successfully'})


@app.route('/record', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({'error': 'Please provide user_id and/or category_id as parameters'}), 400

    filtered_expenses = expenses
    if user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user_id parameter'}), 400

        filtered_expenses = [e for e in filtered_expenses if e['user_id'] == user_id]
    if category_id:
        try:
            category_id = int(category_id)
        except ValueError:
            return jsonify({'error': 'Invalid category_id parameter'}), 400

        filtered_expenses = [e for e in filtered_expenses if e['category_id'] == category_id]

    return jsonify(filtered_expenses)













