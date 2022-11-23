import sqlite3
from contextlib import closing

from functionalModule import func_students

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

connection = sqlite3.connect('academic-performance.db', check_same_thread=False)
with closing(connection.cursor()) as cursor:
    cursor.execute("""CREATE TABLE IF NOT EXISTS performance(
       lecture_visits INT(3) NOT NULL DEFAULT 0,
       practice_visits INT(3) NOT NULL DEFAULT 0,
       practice INT(3) NOT NULL DEFAULT 0,
       studentid VARCHAR(8) PRIMARY KEY NOT NULL UNIQUE,
       FOREIGN KEY (studentid) REFERENCES students(studentid)
       );
       """)
connection.commit()
connection.close()
