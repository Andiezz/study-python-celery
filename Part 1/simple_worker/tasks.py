import time
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery_app = Celery(
    "tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)


@celery_app.task()
def longtime_add(x, y):
    logger.info("Got Request - Starting work ")
    time.sleep(4)
    logger.info("Work Finished ")
    return x + y


@celery_app.task()
def return_something():
    print("something")
    return "something"


# error handler task chain
@celery_app.task()
def error_handler(request, exc, traceback):
    print("Task {0} raised exception: {1!r}\n{2!r}".format(request.id, exc, traceback))
