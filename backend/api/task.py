from flask_restful import Resource, request
from models import Task
from extensions import db, cache
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

class TaskResource(Resource):
    @jwt_required()
    @cache.cached(timeout=360)
    def get(self, task_id=None):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if not task_id :
            print("*"*10, user.role)
            if user.role != "admin":
                return {"message": "You are not authorized to access this resource."}, 403

            tasks = Task.query.all()
            data = []
            for task in tasks:
                data.append(task.to_dict())
            print(data)
            return {"message": "all the tasks!", "tasks": data}, 200
        else:
            task = Task.query.get_or_404(task_id)
            print("*"*10, task.assigned_to, user.id)
            if task.assigned_to != user.id and user.role != "admin":
                return {"message": "You are not authorized to access this task."}, 403
            task_data = task.to_dict()
            return {"message": "task record of given task_id", "task": task_data}

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if user.role != "admin":
            return {"message": "You are not authorized to create a task."}, 403
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        assigned_to = data.get("assigned_to")

        task = Task(title=title, description=description, assigned_to=assigned_to)
        db.session.add(task)
        db.session.commit()
        return {"message": "task created!"}, 201

    @jwt_required()
    def put(self, task_id):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if user.role != "admin":
            return {"message": "You are not authorized to update a task."}, 403
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        assigned_to = data.get("assigned_to")

        task = Task.query.get_or_404(task_id)
        task.title = title
        task.description = description
        task.assigned_to = assigned_to

        db.session.commit()
        cache.delete_memoized(self.get, task_id)  # Clear the cache for this specific task
        return {"message":"task updated!!"}
    @jwt_required()
    def delete(self, task_id):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if user.role != "admin":
            return {"message": "You are not authorized to delete a task."}, 403
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message":"task deleted!!"}