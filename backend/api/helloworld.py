from datetime import datetime
from extensions import cache
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class HelloWorld(Resource):
    @cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
    def get(self):
        print("GET request received")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"message": "this is get method!", "time": time_now}, 200

    def post(self):
        return {"message": "Created!"}, 201
    def put(self):
        return {"message": "updated!"}, 201
    
    def delete(self):
        return {"message": "deleted!"}, 201

class DeleteCache(Resource):

    def get(self):
        cache.clear()
        return {"message": "cache cleared!!"}