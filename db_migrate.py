import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
import re

'''reading CSV file and creating a dataframe of it.'''
imported_data = pd.read_csv('/home/ttn/dbmigration/ProjectFiles/dbfile.csv', header = 0)


'''establishes a connection with the database'''
engine = create_engine('mysql+mysqlconnector://root:igdefault@localhost/db_migration')
with engine.connect() as conn, conn.begin():
    imported_data.to_sql('datafile', conn, if_exists='replace', index=False) #inserting the dataframe into the database in a file named 'datafile'

email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

'''prompting user to enter the exchange rate and handling exceptions'''
try:
    USDINR_rate = int(input("Enter the conversion rate USD to INR: "))

except ValueError:
    print("Please enter valid input.")
    exit()

'''reading inputted list from the database'''
reading_data = pd.read_sql_table('datafile',engine)

'''checking email with regular expression'''
for email in range(len(reading_data)):
    pattern=re.search(email_regex,reading_data.iloc[email][4])
    if not pattern:
        print(reading_data.iloc[email][4])
        reading_data.drop(reading_data.iloc[email], axis=4, inplace=True)
with engine.connect() as conn, conn.begin():
    reading_data.to_sql('cleaned_emails_data', conn, if_exists='replace', index=False)


query = f'SELECT CONCAT_WS(" ", first, last) AS Name, age as Age,  street as Location, email as Email, {USDINR_rate}*digit as Salary  FROM cleaned_emails_data;'

'''preparing a clean list from the inputted list based on the query above'''
clean_list = pd.read_sql_query(query, engine)

'''inserting the list back into the database inside a new table: CleanDatafile'''
with engine.connect() as conn, conn.begin():
    clean_list.to_sql('CleanDatafile', conn, if_exists='replace', index=False)





