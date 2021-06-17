# foodgram-project
## Описание проекта
Cайт «Продуктовый помощник»


## Стек технологий
* Python 3.9;
* Django and Django Rest Framework;


### Ручное развертывание
* Склонируйте репозиторий проекта: `git clone https://github.com/Alice15423/foodgram-project.git`
* Перейдите в корневую директорию проекта: `cd foodgram-project`
* Создайте виртуальное окружение: `python -m venv venv`
* Запустите виртуальное окружение: (*windows*) `source venv/Scripts/activate`
* Установите зависимости `pip install -r requirements.txt`
* Инициализируйте пустую базу данных `python ./foodgram/manage.py migrate`
* Создайте суперпользователя `python ./foodgram/manage.py createsuperuser`
* Сделайте сборку статических файлов `python ./foodgram/manage.py collectstatic`
* Запустите локальный сервер `python ./foodgram/manage.py runserver`