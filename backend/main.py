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
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = 'rajnish@local'
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

test_mail_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Welcome aboard!</title>
        </head>
        <body style="margin:0;padding:0;background:#f3f4f6;
                     font-family:Arial,Helvetica,sans-serif;color:#1f2937;">

          <table role="presentation" width="100%" cellspacing="0"
                 cellpadding="0" border="0" style="background:#f3f4f6;">
            <tr>
              <td align="center" style="padding:35px 12px;">

                <table role="presentation" width="600" cellspacing="0"
                       cellpadding="0" border="0"
                       style="max-width:600px;width:100%;background:#ffffff;
                              border-radius:16px;overflow:hidden;">

                  <!-- Gradient-style header -->
                  <tr>
                    <td align="center"
                        style="padding:38px 25px;background:#4f46e5;
                               background-image:linear-gradient(135deg,#4f46e5,#9333ea);
                               color:#ffffff;">
                      <div style="font-size:13px;letter-spacing:3px;
                                  font-weight:bold;color:#e0e7ff;">
                        YOU'RE IN!
                      </div>
                      <h1 style="margin:16px 0 8px;font-size:32px;
                                 line-height:1.25;color:#ffffff;">
                        Welcome aboard! 🎉
                      </h1>
                      <p style="margin:0;font-size:16px;line-height:1.7;
                                color:#ede9fe;">
                        Your next chapter starts here.
                      </p>
                    </td>
                  </tr>

                  <!-- Welcome illustration -->
                  <tr>
                    <td align="center" style="padding:28px 25px 8px;">
                      <img
                        src="https://placehold.co/500x220/e0e7ff/4338ca?text=Great+Things+Start+Here"
                        alt="Great things start here"
                        width="500"
                        style="display:block;width:100%;max-width:500px;
                               height:auto;border:0;border-radius:12px;">
                    </td>
                  </tr>

                  <!-- Main content -->
                  <tr>
                    <td style="padding:22px 35px 12px;">
                      <h2 style="margin:0 0 18px;font-size:24px;
                                 color:#111827;">
                        Hey, 👋
                      </h2>

                      <p style="font-size:16px;line-height:1.8;
                                color:#4b5563;margin:0 0 16px;">
                        We're absolutely delighted to welcome you!
                        Thanks for joining us. We're excited to have
                        you as part of our community.
                      </p>

                      <p style="font-size:16px;line-height:1.8;
                                color:#4b5563;margin:0 0 24px;">
                        Whether you're here to learn something new,
                        explore opportunities, or achieve your next big
                        goal, we're here to help you along the way.
                      </p>

                      <!-- Feature card -->
                      <table role="presentation" width="100%" cellspacing="0"
                             cellpadding="0" border="0"
                             style="background:#f5f3ff;border-radius:12px;">
                        <tr>
                          <td style="padding:22px;">
                            <p style="margin:0 0 12px;font-size:17px;
                                     font-weight:bold;color:#4338ca;">
                              ✨ Here's what awaits you
                            </p>
                            <p style="margin:8px 0;font-size:15px;
                                      line-height:1.7;color:#374151;">
                              🚀 &nbsp; New opportunities to explore
                            </p>
                            <p style="margin:8px 0;font-size:15px;
                                      line-height:1.7;color:#374151;">
                              📚 &nbsp; Resources to help you grow
                            </p>
                            <p style="margin:8px 0;font-size:15px;
                                      line-height:1.7;color:#374151;">
                              🤝 &nbsp; Support whenever you need it
                            </p>
                          </td>
                        </tr>
                      </table>

                      <p style="font-size:16px;line-height:1.8;
                                color:#4b5563;margin:24px 0;">
                        Ready to get started? Take your first step today!
                      </p>

                      <!-- Call-to-action button -->
                      <table role="presentation" cellspacing="0"
                             cellpadding="0" border="0" align="center">
                        <tr>
                          <td align="center" bgcolor="#4f46e5"
                              style="border-radius:8px;">
                            <a href="https://example.com"
                               style="display:inline-block;padding:15px 32px;
                                      color:#ffffff;text-decoration:none;
                                      font-size:16px;font-weight:bold;
                                      border-radius:8px;">
                              Let's Get Started →
                            </a>
                          </td>
                        </tr>
                      </table>

                      <p style="font-size:16px;line-height:1.8;
                                color:#4b5563;margin:28px 0 8px;">
                        If you have any questions, just reply to this email.
                        We'd love to hear from you.
                      </p>

                      <p style="font-size:16px;line-height:1.8;
                                color:#374151;margin:18px 0 0;">
                        Warm regards,<br>
                        <strong style="color:#111827;">The Team</strong>
                      </p>
                    </td>
                  </tr>

                  <!-- Footer -->
                  <tr>
                    <td align="center"
                        style="padding:25px 20px;background:#f9fafb;
                               border-top:1px solid #e5e7eb;">
                      <p style="margin:0 0 8px;font-size:13px;
                                color:#6b7280;">
                        Made with ❤️ and a little excitement.
                      </p>
                      <p style="margin:0;font-size:12px;line-height:1.7;
                                color:#9ca3af;">
                        © 2026 Your Company. All rights reserved.
                      </p>
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

class SendEmails(Resource):
    def get(self):
        msg = Message(
            subject="test email",
            recipients=['22f2000625@ds.study.iitm.ac.in'],
            html=test_mail_html
        )
        with open("welcome.pdf", "rb") as file:
            msg.attach(
                filename="Welcome-Guide.pdf",
                content_type="application/pdf",
                data=file.read()
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