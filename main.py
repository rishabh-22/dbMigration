import sys
import csv
import re
import mysql.connector
from dbconnection import get_connection
from import_data import import_csvdata
from dbmigration import migrate_data

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if (sys.argv[1] == '--import' and (sys.argv[2]).isalpha):
            print ("Importing from CSV, please wait!")
            import_csvdata(sys.argv[2])
        
        elif (sys.argv[1] == '--migrate' and sys.argv[2].isalpha):
            print("Migrating now, please wait!")
            migrate_data()
        
        else:
            print("Something is wrong with the parameters, please check.")

    else:
        print("Please supply some argument to the script.")

else:
    print("Code will not execute unless a file is imported.")
