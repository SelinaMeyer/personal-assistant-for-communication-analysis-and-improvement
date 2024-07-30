To run the app, use the following commands:

docker-compose build   

docker-compose run --rm app sh -c "django-admin startproject app ."

docker-compose run --rm app sh -c "python manage.py startapp survey"

docker-compose run --rm app sh -c "python manage.py makemigrations"

docker-compose run --rm app sh -c "python manage.py migrate"

docker-compose run --rm app sh -c "python manage.py createsuperuser"

docker-compose run --rm app sh -c "python manage.py runserver"
