from flask import Flask
from mongoengine import connect


app = Flask(__name__)
connect(db='mydatabase', host='mongodb://mongo:27017/mydatabase')


import app_module.views
if __name__ == '__main__':
    app.run(debug=True)


