# Парсер HTML-страниц с заданной глубиной поиска и количеством одновременно загружаемых страниц.

Приложение реализовано на фреймворке FastApi, страницы сохраняются в БД mongodb.
Для запуска приложения необходимо выполнить команду `docker-compose up`.

Протестировать можно в разделе документации по адресу `0.0.0.0:8080/docs`.

Реализованы все основные требования + добавлены линтеры пре-коммита, в т.ч. `mypy`.

К сожалению, не хватает времени настроить тестирование.