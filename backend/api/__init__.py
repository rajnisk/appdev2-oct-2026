from api.helloworld import HelloWorld
from api.task import TaskResource
from api.auth import Register
from api.auth import Login
def register_routes(api):
    api.add_resource(HelloWorld, "/helloworld")
    api.add_resource(TaskResource, "/task/<int:task_id>", "/tasks")
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")