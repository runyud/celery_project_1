import os
import time
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcelery.settings")
app = Celery("dcelery")
app.config_from_object("django.conf:settings", namespace="CELERY")

# rabbitmq config
app.conf.task_queues = [
    Queue(
        "tasks",
        Exchange("tasks"),
        routing_key="tasks",
        queue_arguments={"x-max-priority": 10},
    ),
]

app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1


@app.task(queue="tasks")
def t1(a, b, message=None):
    time.sleep(3)
    result = a + b
    if message:
        result = f"{message}: {result}"
    return result


@app.task(queue="tasks")
def t2():
    time.sleep(3)
    return


@app.task(queue="tasks")
def t3():
    time.sleep(3)
    return


# redis configs
# app.conf.task_routes = {
#     "newapp.tasks.task1": {"queue": "queue1"},
#     "newapp.tasks.task2": {"queue": "queue2"},
# }
# app.conf.task_default_rate_limit = '1/m'
# app.conf.broker_transport_options = {
#     "priority_steps": list(range(10)),
#     "step": ":",
#     "queue_order_strategy": "priority",
# }

app.autodiscover_tasks()


def test():
    # Call the task asynchronously
    result = t1.apply_async(args=[5, 10], kwargs={"message": "The sum is"})

    # check if the task has completed
    if result.ready():
        print("Task has completed")
    else:
        print("Task is still running")

    # check if the task completed successfully
    if result.successful():
        print("Task completed successfully")
    else:
        print("Task encountered an error")

    # Get the result of the task
    try:
        task_result = result.get()
        print("Task result:", task_result)
    except Exception as e:
        print("An exception occurred:", str(e))

    # Get the exception (if any) that occurred during task execution
    exception = result.get(propagate=False)
    if exception:
        print("An exception occurred during task execution:", str(exception))

# Synchronous task execution
def execute_sync():
    result = t1.apply_async(args=[5,10], kwargs={"message": "The sum is"})
    task_result = result.get()
    print("Task is running synchronously")
    print(task_result)

# Asynchronous task execution
def execute_async():
    result = t1.apply_async(args=[5,10], kwargs={"message": "The sum is"})
    print("Task is running asynchronously")
    print("Task ID:", result.task_id)
