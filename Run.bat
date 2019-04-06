@echo off
start "HealthNet" "http://127.0.0.1:8000/"
python manage.py migrate
python manage.py makemigrations account
python manage.py makemigrations administration
python manage.py makemigrations appointments
python manage.py makemigrations messenger
python manage.py makemigrations meditems
python manage.py makemigrations login
python manage.py migrate
python manage.py runserver
sleep(3)
start "http://127.0.0.1:8000/"