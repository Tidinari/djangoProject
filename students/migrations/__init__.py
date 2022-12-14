import sqlite3
from contextlib import closing

connection = sqlite3.connect('students.db', check_same_thread=False)
with closing(connection.cursor()) as cursor:
    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
       studentid VARCHAR(8) PRIMARY KEY NOT NULL UNIQUE,
       fname TEXT NOT NULL,
       sname TEXT NOT NULL,
       lname TEXT NOT NULL,
       groupid VARCHAR(10) NOT NULL);
       """)
connection.commit()
connection.close()
