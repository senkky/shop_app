# Практическая работа 2  
# Введение в Django

  

## Практика

### Практика. Видео 1

-   [Методы HTTP-запроса](https://developer.mozilla.org/ru/docs/Web/HTTP/Methods)
    
-   [Заголовки HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP/Headers)
    
-   [Коды ответа HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP/Status)
    

### Практика. Видео 2

-   [Migrations | Django documentation](https://docs.djangoproject.com/en/4.0/topics/migrations/)
    
-   [The Django admin site](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)
    
-   [django-admin and manage.py](https://docs.djangoproject.com/en/4.0/ref/django-admin/)
    

### Практика. Видео 3

-   [URL dispatcher | Django documentation](https://docs.djangoproject.com/en/4.0/topics/http/urls/)
    

### Практика. Видео 4

-   [Templates | Django documentation](https://docs.djangoproject.com/en/4.0/topics/templates/)
    

### Практика. Видео 5

-   [Built-in template tags and filters丨Django documentation](https://docs.djangoproject.com/en/4.0/ref/templates/builtins/)
    

  

## Цели практической работы

-   Создать и запустить Django-приложение.
    
-   Выполнить миграции.
    
-   Создать суперпользователя.
    
-   Описать модель.
    
-   Сгенерировать миграции для созданной модели.
    
-   Выполнить сгенерированные миграции.
    
-   Создать веб-страницу на основе Django-шаблона.
    
-   Вывести на страницу сущности из базы данных.
    

## Что нужно сделать

1.  Создайте проект mysite.
    
2.  Создайте приложение shopapp.
    

Приложение должно быть установлено в настройках.

3.  Создайте модель Product, которая включает поля следующих типов: 
    

-   CharField;
    
-   TextField;
    
-   DecimalField.
    

4.  Выполните стандартные миграции.
    
5.  Создайте и выполните миграции для модели.
    
6.  Создайте пользователя через createsuperuser.
    
7.  Выполните management command в shopapp для создания продуктов через get_or_create (например, create_products.py).
    
8.  Примените view-функции для:
    

-   shop index — списка ссылок на доступные страницы;
    
-   products list — списка продуктов.
    

9.  Подключите view-функции через urls.py внутри приложения.
    

  

## Советы и рекомендации

Если вы работаете через PyCharm, создание и активация виртуального окружения происходит автоматически.

  

## Что оценивается

-   Приложение установлено.
    
-   Модель описана.
    
-   Миграция сгенерирована.
    
-   Django-шаблон создан.
    
-   Маршруты настроены.
    

  

## Как отправить работу на проверку

Сдайте практическую работу этого модуля через систему контроля версий Git сервиса Skillbox GitLab. В материалах с практической работой напишите «Сделано» и прикрепите ссылку на репозиторий.

  