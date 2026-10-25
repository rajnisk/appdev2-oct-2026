from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class HelloWorld(Resource):

    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        print(email)
        return {"message": "this is get method!", "email": email}, 200

    def post(self):
        return {"message": "Created!"}, 201
    def put(self):
        return {"message": "updated!"}, 201
    
    def delete(self):
        return {"message": "deleted!"}, 201
