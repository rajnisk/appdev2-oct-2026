from flask_restful import Resource, request
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "invalid email!"}
        if not check_password_hash(user.password_hash, password):
            return {"message": "invalid password!"}
        token = create_access_token(user.email)
        return {"message": "logged in!", "token":token}


class Register(Resource):
    def post(self):
        data = request.get_json()

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")

        print(full_name, email, password)
        password_hash = generate_password_hash(password)

        user = User(full_name=full_name, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        return {"message": "user registration succesful!"}