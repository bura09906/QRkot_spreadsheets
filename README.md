# QRkot_spreadseets - пример благотворительного сервиса, написанный на FastAPI

Данный проект был написан в рамках кусра Python-разработчик. Основная цель проекта закрепление навыков работы с FastAPI.
Стек: Python 3.9.10, FastAPI, Pydantic, SQLAlchemy, aiogoogle, Alembic

# Инструкция по развертыванию:
# Инструкция по развертыванию:
1. Клонировать репозиторий
2. Создать и активировать виртуальное окружение:

   Команды для Windiws:
   ```
   python -m venv venv
   ```
   ```
   source venv/Scripts/activate
   ```
   Команды для Linux:
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ```
4. Установить зависимости из файла requirements.txt:
   ```
   pip install -r requirements.txt
   ```
5. Находясь в корне проекта запустить работу сервиса командой:
   ```
   uvicorn app.main:app
   ```
