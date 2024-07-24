from flask import Flask
from celery import Celery
from datetime import timedelta


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config["CELERY_BACKEND"] = "redis://redis:6379/0"
app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["CELERY_TIMEZONE"] = "UTC"

celery_app = make_celery(app)

@app.route("/simple_start_task")
def call_method():
    app.logger.info("Invoking Method ")
    #                        queue name in task folder.function name
    r = celery_app.send_task("tasks.longtime_add", kwargs={"x": 1, "y": 2})
    app.logger.info(r.backend)
    return r.id


@app.route("/simple_task_status/<task_id>")
def get_status(task_id):
    status = celery_app.AsyncResult(task_id, app=celery_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route("/simple_task_result/<task_id>")
def task_result(task_id):
    result = celery_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

