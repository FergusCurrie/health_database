'''
This file contains the code to connect to my MySQL instance, and insert all rows after the most recent date
in the database from a dataframe. 
'''

import mysql.connector 
import pandas as pd 
from datetime import datetime

def is_float(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def remove_tz(x):
    '''
    remove time zone. not allowed for datetime. 
    '''
    return ' '.join(x.split(' ')[:2])

def prepare_insert_query(row):
    identifier = row.type
    categorical_value = 'NULL'
    
    # If not a valid float then set to -1. If cateogorical value, add the cateorical value. See readme on why this is necassary.
    numerical_value = -1.0
    if is_float(row.value):
        numerical_value = row.value
    else:
        categorical_value = row.value

    sql = f"INSERT INTO health_records (identifier, creationDate, startDate, endDate, categorical_value, numerical_value) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (identifier, remove_tz(row.creationDate), remove_tz(row.startDate), remove_tz(row.endDate), categorical_value, numerical_value)

    return sql, values

def connect_to_db():
    # open connectoin to db
    mydb = mysql.connector.connect(host="localhost")
    mydb = mysql.connector.connect(
        host="localhost",
        user="fergus",
        database="health_records",
        password=""
    )
    cursor = mydb.cursor()
    return mydb, cursor

def add_records_after_date(df, last_date_in_db, cursor):
    # If there is data in the db already, then only add data that is newer than the most recent date in the db. 
    for i, row in df.iterrows():
        
        if last_date_in_db is not None:
            date_string = row.endDate.replace(' +1300', '')
            date_format = "%Y-%m-%d %H:%M:%S"
            date = datetime.strptime(date_string, date_format)
            # ignore previously entered dates 
            if date <= last_date_in_db:
                continue

        # Add the row to the db.
        sql, values = prepare_insert_query(row)
        cursor.execute(sql, values)

def query_most_recent_date(cursor):
    cursor.execute("SELECT MAX(endDate) AS most_recent_date FROM health_records")
    last_date_in_db = cursor.fetchall()[0][0]
    return last_date_in_db

def pipeline(df):
    '''
    Given a dataframe fill the database with its records,
    providing they are more recent than the most recent record in the database.
    '''

    # Find most recent record
    mydb, cursor = connect_to_db()
    
    # query most recent date, to ignore previously entered dates
    last_date_in_db = query_most_recent_date(cursor)

    # Add records after date 
    add_records_after_date(df, last_date_in_db, cursor)
    

    # Commit and close db connections 
    mydb.commit() # required to actually add the changes 
    cursor.close()
    mydb.close()

if __name__ == "__main__":
    pipeline(fn='/home/fergus/data/project/apple_health_export2.csv')