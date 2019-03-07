import csv
import mysql.connector
from dbconnection import get_connection

'''funnction to get data from the CSV file'''
def import_csvdata(file_name):
    try:
        data = csv.DictReader(open(file_name))
        conn = get_connection()
        cursor = conn.cursor()
        create_table()
    
        for row in data:
            cursor.execute("INSERT INTO imported_data VALUES (%s, %s, %s, %s, %s, %s) ", (row['first'], row['last'], row['age'], row['street'], row['email'], row['digit']))
        conn.commit()

    except ImportError:
        print("File not present in working directory.")

    except mysql.connector.Error:
        print("Failed to insert data into database. {}".format(mysql.connector.Error))

def create_table():
    try: 
        conn = get_connection()
        cursor = conn.cursor()

        create_table_query = 'CREATE TABLE imported_data (Firstname varchar(30), Lastname varchar(30), Age int(2), Location varchar(50), Email varchar(40), Income int(7))'
        cursor.execute(create_table_query)
        conn.commit()
    
    except mysql.connector.Error:
        print("Error encountered while creating table. {}".format(mysql.connector.Error))