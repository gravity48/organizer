# Organizer backend

## Первый запуск проекта

Устанавливаем virtualenv и все зависимости:

```bash
python3.11 -m venv .venv
```

или

```bash
/full/path/to/python3 -m venv .venv
```

Скопировать .env.example в .env и настроить параметры подключения к бд

```bash
cp .env.example .env
```

Заполнить базу данных тестовыми фикстурами

```bash
python manage.py loaddata initial_data.json 
```
