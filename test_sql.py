from sql.validator import validate_sql

print(validate_sql("SELECT * FROM employees"))

print(validate_sql("DROP TABLE employees"))