from flask_restful import Resource

class HelloWorld(Resource):
    def get(self):
        return {"message": "this is get method!"}, 200

    def post(self):
        return {"message": "Created!"}, 201
    def put(self):
        return {"message": "updated!"}, 201
    
    def delete(self):
        return {"message": "deleted!"}, 201
