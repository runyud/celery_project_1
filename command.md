pip freeze > requirements.txt
chmod +x ./entrypoint.sh 
docker-compose up -d --build
./manage.py startapp taskapp
docker exec -it django /bin/sh

# Run on Django to inspect task
celery inspect active
celery inspect active_queues

# Remove all docker
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)

from dcelery.celery import t1,t2,t3
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=9)
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=9)