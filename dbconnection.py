import pandas as pd
import mysql.connector

def get_connection():
    '''this functions establishes a connection to database'''
    try:
        connection = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='dbproject')
        return connection
    except mysql.connector.Error as error:
        print("Encountered error connecting to database. {}" .format(error))

