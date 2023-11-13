pip freeze > requirements.txt
chmod +x ./entrypoint.sh 
docker-compose up -d --build
./manage.py startapp taskapp
docker exec -it django /bin/sh