import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

fake = Faker()

load_dotenv()

def generate_fake_data():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    cur = conn.cursor()

    cur.execute("DELETE FROM employees")
    cur.execute("DELETE FROM departments")
    cur.execute("DELETE FROM projects")

    departments = []
    for _ in range(5):
        cur.execute(
            """INSERT INTO departments 
            (name, budget, established_date, employee_count)
            VALUES (%s, %s, %s, %s) RETURNING id""",
            (fake.company(), 
             random.uniform(10000, 100000), 
             fake.date_between(start_date='-10y', end_date='today'),
             random.randint(5, 50))
        )
        departments.append(cur.fetchone()[0])

    cur.execute("SELECT id FROM departments")
    department_ids = [row[0] for row in cur.fetchall()]

    for _ in range(10):
        cur.execute(
            """INSERT INTO projects 
            (project_name, start_date, end_date, price, status, department_id)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (fake.catch_phrase(), 
            fake.date_this_year(),
            fake.future_date(),
            round(random.uniform(5000, 50000), 2),
            random.choice(['Active', 'Completed', 'Pending']),
            random.choice(department_ids))
        )

    for _ in range(20):
        cur.execute(
            """INSERT INTO employees 
            (full_name, birth_date, salary, department_id, hire_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (fake.name(),
             fake.date_of_birth(minimum_age=18, maximum_age=65),
             round(random.uniform(30000, 120000), 2),
             random.choice(departments),
             fake.date_time_this_decade())
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    generate_fake_data()