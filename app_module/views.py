from flask import jsonify, request
from datetime import datetime
from . import app 
from marshmallow import ValidationError
from .schema import UserSchema, CategorySchema, ExpenseSchema
from .models import User, Category, Expense
from .models import db


user_schema = UserSchema()
category_schema = CategorySchema()
expense_schema = ExpenseSchema()


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
        data = request.get_json()

      
        new_user = User(
            name=data['name'],
            balance=0.0
        )
        
        db.session.add(new_user)
        db.session.commit()

        result = user_schema.dump(new_user)
        return jsonify(result), 201

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)

        if user:
            user_info = user_schema.dump(user)
            return jsonify(user_info)
        else:
            return jsonify({'error': 'User not found'}), 404

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        balance_to_add = user.balance

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully', 'balance_added': balance_to_add})

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_info = [{'id': user.id, 'name': user.name, 'balance': user.balance} for user in users]
        return jsonify(users_info)

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/category', methods=['POST'])
def create_category():
    try:
        data = request.get_json()
        category_data = category_schema.load(data)
        
        category = Category(name=category_data['name'])
        db.session.add(category)
        db.session.commit()

        return jsonify(category_schema.dump(category)), 201

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()

        categories_info = [{'id': category.id, 'name': category.name} for category in categories]

        return jsonify(categories_info)

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)

        if not category:
            return jsonify({'error': 'Category not found'}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': 'Category deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/record', methods=['POST'])
def create_expense():
    try:
        data = request.get_json()

        expense_data = expense_schema.load(data)

        user_id = expense_data['user_id']
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        expense_amount = expense_data['amount']

        if user.balance < expense_amount:
            return jsonify({'error': 'Insufficient balance'}), 400

        user.balance -= expense_amount

        expense = Expense(
            user_id=user_id,
            category_id=expense_data['category_id'],
            amount=expense_amount
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify(expense_schema.dump(expense)), 201

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/record', methods=['GET'])
def get_expenses():
    try:
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')

        if not user_id and not category_id:
            return jsonify({'error': 'Please provide user_id and/or category_id as parameters'}), 400

        if user_id:
            expenses = Expense.query.filter_by(user_id=int(user_id)).all()
        elif category_id:
            expenses = Expense.query.filter_by(category_id=int(category_id)).all()
        else:
            expenses = Expense.query.all()

        return jsonify(expense_schema.dump(expenses, many=True))

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/record/<int:record_id>', methods=['GET'])
def get_expense(record_id):
    try:
        expense = Expense.query.get(record_id)

        if expense:
            return jsonify(expense_schema.dump(expense))
        else:
            return jsonify({'error': 'Record not found'}), 404

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_expense(record_id):
    try:
        expense = Expense.query.get(record_id)

        if expense:
            db.session.delete(expense)
            db.session.commit()
            return jsonify({'message': 'Record deleted successfully'})
        else:
            return jsonify({'error': 'Record not found'}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@app.route('/income/<int:user_id>', methods=['POST'])
def add_income(user_id):
    try:
        data = request.get_json()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        income_amount = data.get('amount', 0.0)

        if income_amount <= 0:
            return jsonify({'error': 'Invalid income amount'}), 400

        user.balance += income_amount

        db.session.commit()  

        return jsonify({'message': 'Income added successfully', 'new_balance': user.balance})

    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500











