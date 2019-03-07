import re
import csv
import sys
import mysql.connector
from dbconnection import get_connection

'''Migrates data from imported table into a new table after all the required processing'''
def migrate_data():
    try:
        conn = get_connection()
        cursor = conn.cursor
        select_query = 'SELECT * FROM imported_data'
        cursor.execute(select_query)
        data = cursor.fetchall()
        create_clean_table()
        email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        exchange_rate = int(input("Enter the current exchange rate USD to INR: "))

        for row in data:
            new_data = {}
            new_data['Name'] = row[0]+row[1]
            new_data['Age'] = row[2]
            new_data['Location'] = row[3]
            new_data['Email'] = row[4]
            new_data['Income'] = row[5]

            notmatched = False
            pattern = re.search(email_regex, row[4])
            if pattern == None:
                notmatched = True
                print (new_data['Email'], new_data['Name'], new_data['Age'], new_data['Location'], new_data['Income'])
            income_INR = new_data['Income'] * exchange_rate
            if not notmatched:
                cursor.execute("INSERT INTO filtered_data VALUES (%s, %s, %s, %s, %s) ", (new_data['Name'], new_data['Age'], new_data['Location'], new_data['Email'], income_INR))
        conn.commit()
    except mysql.connector.Error:
        print("Encountered error {}".format(mysql.connector.Error))

def create_clean_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        create_query = 'CREATE TABLE filtered_data(Name varchar(60), Age int(2), Location varchar(50), Email varchar(40), Income int(7))'
        cursor.execute(create_query)
        conn.commit()
    except mysql.connector.Error:
        print("Encountered error while creating table {}".format(mysql.connector.Error))
