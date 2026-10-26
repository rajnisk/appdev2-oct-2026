import os
from flask import Flask, request
from flask_restful import Api, Resource
from flask_mail import Mail, Message
from flask_caching import Cache
from celery import Celery
from dotenv import load_dotenv
from celery.schedules import crontab
from datetime import datetime

# Load .env
load_dotenv()

app = Flask(__name__)
api = Api(app)

# ============================
# Flask-Mail Configuration
# ============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')
mail = Mail(app)

# ============================
# Flask-Caching with Redis
# ============================
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 1
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60
cache = Cache(app)

# ============================
# Celery Configuration
# ============================
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['broker_url'], backend=app.config['result_backend'])
celery.conf.broker_connection_retry_on_startup = True

# ============================
# Celery Context Setup
# ============================
def init_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['broker_url'],
        backend=flask_app.config['result_backend']
    )
    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

celery = init_celery(app)

class SendEmails(Resource):
    def get(self):
        msg = Message(
            subject="test email",
            recipients=['22f2000625@ds.study.iitm.ac.in'],
            body="test"
        )
        mail.send(msg)
        return {"message":"mail sent!!"}

class CacheDemo(Resource):
    @cache.cached()
    def get(self):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {'data': 'This is a cached response!', 'time': time_now}, 200
class DeleteCache(Resource):
    def post(self):
        cache.clear()
        return {'message': 'Cache cleared successfully!'}, 200

class MonthlyReport(Resource):
    def get(self):
        task = monthly_report.apply_async()
        return {"message":"you will receive an email once the report is ready", "task_id":task.id}
api.add_resource(DeleteCache, '/delete-cache')
api.add_resource(CacheDemo, '/cache')
api.add_resource(SendEmails, "/send_emails")
api.add_resource(MonthlyReport, "/monthly_report")





# ============================
# schedules
# ============================
celery.conf.timezone = 'Asia/Kolkata'
celery.conf.beat_schedule = {
    'monthly-report': {
        'task': 'tasks.monthly_report',
        'schedule': crontab(day_of_month=26, hour=8, minute=29),
    },
    'daily-reminder': {
        'task': 'tasks.daily_reminder',
        'schedule': crontab(hour=8, minute=29),
    },
}



# ============================
# Celery tasks
# ============================
@celery.task(name="tasks.background_task")
def background_task():
    return 'Background task completed'

@celery.task(name="tasks.monthly_report")
def monthly_report():
    return {"message":"this is monthly report"}
@celery.task(name="tasks.daily_reminder")
def daily_reminder():
    return {"message":"this is a daily reminder"}

if __name__=="__main__":
    app.run(debug=True)