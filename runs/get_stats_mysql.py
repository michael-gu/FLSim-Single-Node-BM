import mysql.connector
from flsim.mysql_database_helper import get_benchmark_stats

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='michgu',
    password='Dolphin#1',
    database='benchmarks'
)

# Create a cursor object
cursor = conn.cursor()

# Execute the query to get all table names
cursor.execute("SHOW TABLES")

# Fetch all the results
tables = cursor.fetchall()

# For each table
for table in tables:
    table_name = table[0]
    print(f"{table_name} exists")
    csv_path = f"../benchmark_stats/{table_name}.csv"
    
    # Call get_benchmark_stats for each table
    get_benchmark_stats('localhost', 'michgu', 'Dolphin#1', 'benchmarks', table_name, csv_path)

# Close the connection
conn.close()