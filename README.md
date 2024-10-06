# Анализатор логов nginx

Скрипт читает лог,
парсит нужные поля, считает необходимую статистику по
url’ам и рендерит шаблон

### Примеры использования
С пользовательским файлом конфигурации:

`python3 log_analyzer.py --config config.json`

С файлом конфигурации по умолчанию (config.json):

`python3 log_analyzer.py`

### Testing
`python3 -m unittest`