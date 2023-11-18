from celery import group
from dcelery.celery_config import app

app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True

@app.task(queue='tasks')
def my_task(z):
    try:
        if z == 2:
            raise ValueError("Error wrong number")
    except Exception as e:
        handle_failed_task.apply_async(args=(z, str(e)))
        raise e

@app.task(queue="dead_letter")
def handle_failed_task(z, exception):
    return "Custom Logic to process"


def run_task_group():
    task_group = group(
        my_task.s(1),
        my_task.s(2),
        my_task.s(3),
    )
    task_group.apply_async()
