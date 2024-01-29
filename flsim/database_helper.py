import csv
import pickle
import sqlite3
import os

def insert_model(db_path, table, model_state_dict, client_id, global_epoch_num, global_round_num):
    dir_path = os.path.dirname(db_path)
    if not os.path.exists(dir_path):
        # Create the directory
        os.makedirs(dir_path)

    connection = sqlite3.connect(db_path);
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "{}" (
            model BLOB,
            client_id INTEGER,
            global_epoch_num INTEGER,
            global_round_num INTEGER
        )
    '''.format(table))
    connection.commit()

    model_blob = pickle.dumps(model_state_dict)
    cursor.execute('''
        INSERT INTO "{}"(model, client_id, global_epoch_num, global_round_num)
        VALUES(?, ?, ?, ?)
    '''.format(table), (model_blob, client_id, global_epoch_num, global_round_num))
    connection.commit()
    connection.close()

def insert_completed_model(db_path, table, model_state_dict, timestamp):
    connection = sqlite3.connect(db_path);
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "{}" (
            model BLOB,
            timestamp TEXT
        )
    '''.format(table))
    connection.commit()

    model_blob = pickle.dumps(model_state_dict)
    cursor.execute('''
        INSERT INTO "{}"(model, timestamp)
        VALUES(?, ?)
    '''.format(table), (model_blob, timestamp))
    connection.commit()
    connection.close()

def get_completed_model(db_path, table, timestamp):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT model FROM "{}" WHERE timestamp = "{}"
    '''.format(table, timestamp))
    model_blob = cursor.fetchone()[0]
    
    connection.commit()
    connection.close()

    return pickle.loads(model_blob)

def get_db_size(db_path):
    size = os.path.getsize(db_path)
    return size

def delete_table(db_path, table):
    # Check if the directory exists
    dir_path = os.path.dirname(db_path)
    if not os.path.exists(dir_path):
        # Create the directory
        os.makedirs(dir_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS "{}"
    '''.format(table))
    connection.commit()
    connection.close()

def clear_model_db(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        if table_name[0] != 'sqlite_sequence':
            cursor.execute('DROP TABLE IF EXISTS "{}"'.format(table_name[0]))
            connection.commit()
    connection.commit()
    connection.close()

def insert_benchmark_stats(db_path, table, global_num_epoch, client_num_epoch, num_users, users_per_round, tracking_data_provenance, training_time, model_storage_size):
    dir_path = os.path.dirname(db_path)
    if not os.path.exists(dir_path):
        # Create the directory
        os.makedirs(dir_path)
    
    connection = sqlite3.connect(db_path);
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "{}" (
            itr_id INTEGER PRIMARY KEY AUTOINCREMENT,
            global_num_epoch INTEGER,
            client_num_epoch INTEGER,
            num_users INTEGER,
            users_per_round INTEGER,
            tracking_data_provenance BOOLEAN,
            training_time REAL,
            model_storage_size INTEGER
        )
    '''.format(table))
    connection.commit()

    cursor.execute('''
        INSERT INTO "{}" ("global_num_epoch", "client_num_epoch", "num_users", "users_per_round", "tracking_data_provenance", "training_time", "model_storage_size")
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''.format(table), (global_num_epoch, client_num_epoch, num_users, users_per_round, tracking_data_provenance, training_time, model_storage_size))

    connection.commit()
    connection.close()

def get_benchmark_stats(db_path, table, csv_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM "{}"
    '''.format(table))
    stats = cursor.fetchall()

    connection.commit()
    connection.close()

    # Check if the directory exists and create it if it doesn't
    dir_path = os.path.dirname(csv_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write the stats to a CSV file
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(stats)

