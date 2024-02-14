import csv
import json
import pickle
import os
import mysql.connector

def insert_model(db_host, db_user, db_password, db_name, table, model_state_dict, client_id, global_epoch_num, global_round_num):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `{}` (
            itr_id INT AUTO_INCREMENT PRIMARY KEY,
            model LONGBLOB,
            client_id TEXT,
            global_epoch_num INTEGER,
            global_round_num INTEGER
        )       
    '''.format(table))
    connection.commit()

    model = pickle.dumps(model_state_dict)

    cursor.execute('''
        INSERT INTO `{}`(model, client_id, global_epoch_num, global_round_num)
        VALUES(%s, %s, %s, %s)
    '''.format(table), (model, client_id, global_epoch_num, global_round_num))
        
    connection.commit()
    connection.close()

def insert_model_crypto(db_host, db_user, db_password, db_name, table, model_hash, client_id, global_epoch_num, global_round_num):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `{}` (
            itr_id INT AUTO_INCREMENT PRIMARY KEY,
            model_hash TEXT,
            client_id TEXT,
            global_epoch_num INTEGER,
            global_round_num INTEGER
        )       
    '''.format(table))
    connection.commit()

    cursor.execute('''
        INSERT INTO `{}`(model_hash, client_id, global_epoch_num, global_round_num)
        VALUES(%s, %s, %s, %s)
    '''.format(table), (model_hash, client_id, global_epoch_num, global_round_num))
        
    connection.commit()
    connection.close()

def insert_model_encrypted(db_host, db_user, db_password, db_name, table, encrypted_model, encryption_time):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `{}` (
            itr_id INT AUTO_INCREMENT PRIMARY KEY,
            encrypted_model LONGBLOB,
            encryption_time REAL
        )       
    '''.format(table))
    connection.commit()

    cursor.execute('''
        INSERT INTO `{}`(encrypted_model, encryption_time)
        VALUES(%s, %s)
    '''.format(table), (encrypted_model, encryption_time))
        
    connection.commit()
    connection.close()

def insert_completed_model(db_host, db_user, db_password, db_name, table, model_state_dict, timestamp):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `{}` (
            model BLOB,
            timestamp TEXT
        )
    '''.format(table))
    connection.commit()

    model_blob = pickle.dumps(model_state_dict)
    cursor.execute('''
        INSERT INTO `{}`(model, timestamp)
        VALUES(%s, %s)
    '''.format(table), (model_blob, timestamp))
    connection.commit()
    connection.close()

def get_completed_model(db_host, db_user, db_password, db_name, table, timestamp):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        SELECT model FROM `{}` WHERE timestamp = %s
    '''.format(table), (timestamp,))
    model_blob = cursor.fetchone()[0]
    
    connection.commit()
    connection.close()

    return pickle.loads(model_blob)

def get_table_size(db_host, db_user, db_password, db_name, table_name):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        SELECT table_name AS `Table`, 
               ROUND((data_length + index_length) / 1024 / 1024, 2) AS `Size (MB)` 
        FROM information_schema.TABLES 
        WHERE table_schema = %s AND table_name = %s;
    ''', (db_name, table_name,))
    size = cursor.fetchone()[1]
    
    connection.commit()
    connection.close()

    return size

def delete_table(db_host, db_user, db_password, db_name, table):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS `{}` 
    '''.format(table))
    connection.commit()
    connection.close()

def clear_model_db(db_host, db_user, db_password, db_name):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table_name in tables:
        table_name = table_name[0]
        if table_name != 'sqlite_sequence':
            cursor.execute('DROP TABLE IF EXISTS `{}`'.format(table_name))
            connection.commit()
    connection.commit()
    connection.close()

def insert_benchmark_stats(db_host, db_user, db_password, db_name, table, global_num_epoch, client_num_epoch, num_users, users_per_round, tracking_data_provenance, training_time, model_storage_size):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `{}` (
            itr_id INT AUTO_INCREMENT PRIMARY KEY,
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
        INSERT INTO `{}` (`global_num_epoch`, `client_num_epoch`, `num_users`, `users_per_round`, `tracking_data_provenance`, `training_time`, `model_storage_size`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''.format(table), (global_num_epoch, client_num_epoch, num_users, users_per_round, tracking_data_provenance, training_time, model_storage_size))

    connection.commit()
    connection.close()

def get_benchmark_stats(db_host, db_user, db_password, db_name, table, csv_path):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM `{}` 
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
