from flask_restful import Resource, request
from models import Task
from extensions import db

class TaskResource(Resource):
    def get(self, task_id=None):
        if not task_id:
            tasks = Task.query.all()
            data = []
            for task in tasks:
                data.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "assigned_to": task.assigned_to
                })
            print(data)
            return {"message": "all the tasks!", "tasks": data}, 200
        else:
            task = Task.query.get_or_404(task_id)
            task_data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "assigned_to": task.assigned_to
            }
            return {"message": "task record of given task_id", "task": task_data}

    def post(self):
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        assigned_to = data.get("assigned_to")

        task = Task(title=title, description=description, assigned_to=assigned_to)
        db.session.add(task)
        db.session.commit()
        return {"message": "task created!"}, 201

    def put(self, task_id):
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        assigned_to = data.get("assigned_to")

        task = Task.query.get_or_404(task_id)
        task.title = title
        task.description = description
        task.assigned_to = assigned_to

        db.session.commit()
        return {"message":"task updated!!"}

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message":"task deleted!!"}