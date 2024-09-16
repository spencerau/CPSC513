import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

#Make Connection
conn = mysql.connector.connect(host="localhost",
user="root",
password=os.getenv("PASSWORD"),
auth_plugin='mysql_native_password')

#create cursor object
cur_obj = conn.cursor()

#create database schema
#cur_obj.execute("CREATE SCHEMA MyTestSchema;")

#confirm execution worked by printing result
# cur_obj.execute("SHOW DATABASES;")
# for row in cur_obj:
#     print(row)


cur_obj.execute('''
                CREATE TABLE IF NOT EXISTS 
                ''')

#Print out connection to verify and close
print(conn)
conn.close()