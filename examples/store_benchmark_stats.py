from flsim.database_helper import get_benchmark_stats
import sqlite3

# Connect to the database
conn = sqlite3.connect('benchmark_databases/cifar10_benchmarks.db')

# Create a cursor object
cursor = conn.cursor()

# Execute the query to check if the table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='benchmarks_yes_tracking'")

# Fetch the result
result = cursor.fetchone()

# Check if the table exists
if result:
    print("benchmarks_yes_tracking exists")
    csv_path = "../benchmark_stats/single-node-with-feature.csv"
    get_benchmark_stats('benchmark_databases/cifar10_benchmarks.db', 'benchmarks_yes_tracking', csv_path)
else:
    print("benchmarks_yes_tracking does not exist")


# Execute the query to check if the table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='benchmarks_no_tracking'")

# Fetch the result
result = cursor.fetchone()

# Check if the table exists
if result:
    print("benchmarks_no_tracking exists")
    csv_path = "../benchmark_stats/single-node-without-feature.csv"
    get_benchmark_stats('benchmark_databases/cifar10_benchmarks.db', 'benchmarks_no_tracking', csv_path)
else:
    print("benchmarks_no_tracking does not exist")
# Close the cursor and connection
cursor.close()
conn.close()



