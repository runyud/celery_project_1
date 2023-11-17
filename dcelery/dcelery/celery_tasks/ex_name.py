from dcelery.celery_config import app

@app.task(queue='tasks')
def task_1():
    pass

@app.task(queue='tasks')
def task_2():
    pass