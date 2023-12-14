from flask import jsonify, request
from app_module import app 

users = []
categories = []
expenses = []


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
        'name': data['name']
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


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return jsonify({'message': 'User deleted successfully'})


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)



