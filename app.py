from flask import Flask, render_template, request, send_file
import psycopg2
from openpyxl import Workbook
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_data(filters=None, sort=None):
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    
    # Основной запрос
    base_query = """
    SELECT 
        e.id, 
        e.full_name, 
        e.salary, 
        d.name as department,
        p.project_name,
        p.status as project_status
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    LEFT JOIN projects p ON d.id = p.department_id
    """
    
    conditions = []
    params = []
    
    # Фильтры
    if filters:
        # Фильтр по имени
        if 'name' in filters and filters['name']:
            conditions.append("e.full_name ILIKE %s")
            params.append(f"%{filters['name']}%")
        
        # Фильтр по минимальной зарплате
        if 'min_salary' in filters and filters['min_salary']:
            try:
                min_salary = float(filters['min_salary'])
                conditions.append("e.salary >= %s")
                params.append(min_salary)
            except ValueError:
                pass
        
        # Фильтр по статусам проектов
        if 'statuses' in filters and filters['statuses']:
            conditions.append("p.status IN %s")
            params.append(tuple(filters['statuses']))
        
        # Фильтр по отделу
        if 'department' in filters and filters['department']:
            conditions.append("d.id = %s")
            params.append(filters['department'])
    
    # Сборка условий
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    # Сортировка
    if sort:
        base_query += f" ORDER BY {sort}"
    
    cur.execute(base_query, params)
    columns = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    
    # Получение отделов для фильтра
    cur.execute("SELECT id, name FROM departments")
    departments = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return columns, data, departments

@app.route('/', methods=['GET', 'POST'])
def index():
    filters = {}
    sort = None
    departments = []

    if request.method == 'POST':
        # Фильтры
        filters = {
            'name': request.form.get('name', ''),
            'min_salary': request.form.get('min_salary', ''),
            'statuses': request.form.getlist('statuses'),
            'department': request.form.get('department', '')
        }
        
        # Сортировка
        sort = request.form.get('sort', None)
    
    columns, data, departments = get_data(filters, sort)
    return render_template(
        'index.html',
        columns=columns,
        data=data,
        departments=departments,
        current_filters=filters,
        current_sort=sort
    )

@app.route('/export', methods=['POST'])
def export():
    export_all = request.form.get('export_all') == 'true'
    
    if export_all:
        # Экспорт всех данных без фильтров
        columns, data, _ = get_data()
    else:
        # Получаем текущие фильтры из формы
        filters = {
            'name': request.form.get('name', ''),
            'min_salary': request.form.get('min_salary', ''),
            'statuses': request.form.getlist('statuses'),
            'department': request.form.get('department', '')
        }
        sort = request.form.get('sort', None)
        
        # Получаем отфильтрованные данные
        columns, data, _ = get_data(filters, sort)
    
    # Создание Excel файла
    wb = Workbook()
    ws = wb.active
    ws.append(columns)
    
    for row in data:
        # Преобразование None в пустые строки
        cleaned_row = [cell if cell is not None else "" for cell in row]
        ws.append(cleaned_row)
    
    filename = 'filtered_export.xlsx'
    wb.save(filename)
    
    return send_file(
        filename,
        as_attachment=True,
        download_name="export.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == '__main__':
    app.run(debug=True)