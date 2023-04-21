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

docker-compose logs -f - просмотр logs

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

https://www.django-rest-framework.org/ - сайт drf

https://django-extensions.readthedocs.io/ (django-extensions --group dev) - расширяет возможности manage.py

kwargs['style'] = {'input_type': 'password'} - html стили, в данном случае для замены символов при вводе пароля

docker-compose up -d db - запускаем контейнеры

python manage.py shell_plus - просмотр базы, User.objects.all() - выводим список пользователей

tu = User.objects.last() - присматриваем переменной последнего пользователя, tu.password - смотрим пароль

poetry add social-auth-app-django - для регистрации по VK

python manage.py startapp goals todolist/goals - создание нового app

def validate_category - валидация, после символа нижнего подчеркивания то, что мы валидируем.

with transaction.atomic(): - контекстный менеджер, для того чтобы либо все команды выполнились, либо все не выполнились, если одна или несколько из них упали с ошибкой.

null=True - добавляем параметр после изменений в модели для избежания конфликта с уже созданными миграциями, после заполнения
пустой миграции с добавлением досок убираем этот параметр.

python manage.py makemigrations goals --empty -n create_new_objects - создание пустой миграции

objects.bulk_create - передает список объектов пока еще не созданных в БД
