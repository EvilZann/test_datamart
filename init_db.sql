CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    budget DECIMAL(15,2),
    established_date DATE,
    employee_count INT
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE,
    salary DECIMAL(10,2),
    department_id INT REFERENCES departments(id),
    hire_date TIMESTAMP
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    start_date DATE,
    end_date DATE,
    price NUMERIC(12,2),
    status VARCHAR(50)
);