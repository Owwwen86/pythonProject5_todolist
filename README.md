Todolist + веб-приложение — планировщик задач

(python3.11, Django==4.1.7, Postgres)

django-admin startproject todolist .

pip install requirements.txt - создание файла зависимостей

docker-compose up -d db

docker-compose ps -a - покажет параметры контейнера

python manage.py makemigrations --dry-run (--dry-run - говорит о том, что будет создано)

python manage.py makemigrations

python manage.py migrate - накатить миграции

python manage.py createsuperuser - создание суперюзера

list_display = ('username', 'email', 'first_name', 'last_name') - переопределение столбцов в админке

https://pre-commit.com/

git add .

git status - смотрим файлы перед отправкой

git rm --cashed {файл/папка} - убираем из списка

git commit -m '{название коммита}'

entrypoint.sh - для накатывания миграций

docker-compose build - поднимаем докер файл

docker pull python:3.11.2-slim

poetry export -f requirements.txt -o requirements.txt

docker-compose logs -f

docker-compose exec api /bin/bash - заходим внутрь контейнера

ls -la - смотрим содержимое

docker-compose down 

docker-compose up --build - пересоберём контейнер

 volumes:
      - ./todolist:/opt/todolist/ - при изменении будет перезапускаться

docker-compose ps - смотрим состояние

docker-compose exec frontend /bin/sh - переходим в контейнер фронтенда

cd /etc/nginx/conf.d

python manage.py collectstatic -c - собираем статику (-c  -флаг для перезаписи)

poetry add ansible-vault-win --group dev - библиотека для передачи secrets 

ansible-vault-win -утилита для шифровки файла

ansible-vault encrypt (шифруем) decrypt (дешифруем)
