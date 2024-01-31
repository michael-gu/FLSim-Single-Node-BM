import datetime
import mysql.connector
from flsim.mysql_database_helper import get_benchmark_stats

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='michgu',
    password='Dolphin#1',
    database='cifar10_benchmarks'
)

# Create a cursor object
cursor = conn.cursor()

# Execute the query to check if the table exists
cursor.execute("SHOW TABLES LIKE 'benchmarks_yes_tracking'")

# Fetch the result
result = cursor.fetchone()

currTime = datetime.now()
formatted_time = currTime.strftime("%m-%d-%Y_%H-%M-%S")

# Check if the table exists
if result:
    print("benchmarks_yes_tracking exists")
    csv_path = "../benchmark_stats/single-node-with-feature_" + formatted_time + ".csv"
    get_benchmark_stats('localhost', 'michgu', 'Dolphin#1', 'cifar10_benchmarks', 'benchmarks_yes_tracking', csv_path)
else:
    print("benchmarks_yes_tracking does not exist")


# Execute the query to check if the table exists
cursor.execute("SHOW TABLES LIKE 'benchmarks_no_tracking'")

# Fetch the result
result = cursor.fetchone()

# Check if the table exists
if result:
    print("benchmarks_no_tracking exists")
    csv_path = "../benchmark_stats/single-node-without-feature_" + formatted_time + ".csv"
    get_benchmark_stats('localhost', 'michgu', 'Dolphin#1', 'cifar10_benchmarks', 'benchmarks_no_tracking', csv_path)
else:
    print("benchmarks_no_tracking does not exist")

# Close the connection
conn.close()