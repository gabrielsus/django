@echo off
echo Levantando Django con Docker...
docker run --rm -p 8000:8000 --env-file .env django python manage.py runserver 0.0.0.0:8000
pause