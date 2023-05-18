import mysql.connector 


mydb = mysql.connector.connect(host="localhost")

mydb = mysql.connector.connect(
  host="localhost",
  user="fergus",
  database="health_records",
  password=""
)