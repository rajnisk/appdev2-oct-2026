from flask import Flask, request
from flask_restful import Api, Resource
from extensions import db, jwt
from models import Task, User
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!


api = Api(app)
db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

from api import register_routes

register_routes(api)


if __name__ == "__main__":
    app.run(debug=True)