### Требования
- Python 3.10+
- PostgreSQL 15+

### Установка
1. Клонировать репозиторий:
```bash
git clone https://github.com/EvilZann/test_datamart.git
cd test_datamart 
```

2. Установить зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
3. Создать .env файл, вставить соответствующие значения:
```ini
DB_NAME='company_db'
DB_USER=''
DB_PASSWORD=''
DB_HOST='localhost'
DB_PORT='5432'
SECRET_KEY=''
```

3. Настроить БД
```bash
# Создание БД
createdb company_db
psql -d company_db -f init_db.sql

# Заполнение БД тестовыми данными
python generate_data.py
```

4. Запуск
```bash
export FLASK_APP=app.py  # Linux/Mac
set FLASK_APP=app.py     # Windows
flask run
```
