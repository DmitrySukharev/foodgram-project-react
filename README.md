# Проект Foodgram
Онлайн-сервис рецептов, API для него, "Продуктовый помощник"

## Функциональность сервиса
- Регистрация пользователей
- Публикация рецептов
- Подписка на авторов лучших рецептов
- Добавление рецептов в список "Избранное"
- Добавление рецептов в список покупок
- Генерация списка ингредиентов для рецептов из корзины

### Технологии
Python 3.7+  
Django 3.2.16  
Django Rest Framework 3.12.4  
Djoser 2.1.0  
PostgreSQL 15

### Как запустить проект в режиме отладки:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/DmitrySukharev/api_final_yatube
```

```
cd foodgram-project-react
```
Запустить Docker, перейти в папку infra, запустить Docker контейнеры:
```
docker-compose up
```

Перейти в папку backend, создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции моделей данных и загрузку необходимых компонентов (теги, ингредиенты):

```
python manage.py migrate
```
Создать администратора (суперюзера)
```
python manage.py createsuperuser
```
Собрать статику
```
python manage.py collectstatic
```

Запустить Django:

```
python manage.py runserver
```
После этого проект доступен по адресу http://127.0.0.1/

### Авторы
Дмитрий Сухарев (backend)