import sqlite3
from contextlib import closing

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
