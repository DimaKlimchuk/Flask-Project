from flask import jsonify, request
from datetime import datetime
from app_module import app 


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
    data = request.get_json()
    user = {
        'id': len(users) + 1,
        'name': data['name'],
        'balance': 0.0,
    }
    users.append(user)
    return jsonify(user), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/user/<int:user_id>/update_balance', methods=['POST'])
def update_balance(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        data = request.get_json()
        amount = data.get('amount', 0.0)
        user['balance'] += amount
        return jsonify({'message': f'Balance updated successfully. New balance: {user["balance"]}'})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return jsonify({'message': 'User deleted successfully'})


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    category = {
        'id': len(categories) + 1,
        'name': data['name']
    }
    categories.append(category)
    return jsonify(category), 201


@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)


@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    global categories
    categories = [category for category in categories if category['id'] != category_id]
    return jsonify({'message': 'Category deleted successfully'})


@app.route('/record', methods=['POST'])
def create_expense():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')

    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        if user['balance'] >= amount:
            expense = {
                'id': len(expenses) + 1,
                'user_id': user_id,
                'category_id': data.get('category_id'),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'amount': amount
            }

            expenses.append(expense)
            user['balance'] -= amount

            return jsonify({'message': 'Expense recorded successfully', 'user_balance': user['balance']}), 201
        else:
            return jsonify({'error': 'Insufficient funds'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404



@app.route('/record/<int:record_id>', methods=['GET'])
def get_expense(record_id):
    record = next((expense for expense in expenses if expense['id'] == record_id), None)
    if record:
        return jsonify(record)
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
        filtered_expenses = [expense for expense in filtered_expenses if expense['user_id'] == int(user_id)]
    if category_id:
        filtered_expenses = [expense for expense in filtered_expenses if expense['category_id'] == int(category_id)]

    return jsonify(filtered_expenses)













