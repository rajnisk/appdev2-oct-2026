from datetime import timedelta

from flask import Flask, request
from flask_restful import Api, Resource
from extensions import db, jwt, cache
from models import Task, User
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

os.getenv("name")
print("ENV NAME:", os.getenv("name"))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    

# ============================
# Flask-Caching with Redis
# ============================
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 1
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60



api = Api(app)
db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

def create_admin_user():
    admin = User.query.filter_by(email="admin@local").first()
    if not admin:
        admin = User(full_name="Admin User", email="admin@local", password_hash="admin", role="admin")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

with app.app_context():
    # db.drop_all()  # Drop all tables (use with caution)
    db.create_all()
    create_admin_user()



from api import register_routes

register_routes(api)


if __name__ == "__main__":
    app.run(debug=True)