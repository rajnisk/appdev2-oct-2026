from flask_restful import Resource

class Examination(Resource):
    def get(self):
        return {"message": "Examination GET endpoint"}
    def post(self):
        return {"message": "Examination POST endpoint"}
    def put(self):
        return {"message": "Examination PUT endpoint"}
    def delete(self):
        return {"message": "Examination DELETE endpoint"}