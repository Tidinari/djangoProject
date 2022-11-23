import sqlite3
from contextlib import closing
import json

connection = sqlite3.connect('academic-performance.db', check_same_thread=False)


# Create (insert) operation - C
def insert_student(studentid):
    with closing(connection.cursor()) as cursor:
        result = cursor.execute(f"INSERT INTO performance(studentid) VALUES (?);", (studentid,))
        result = result.fetchone() is not None
    connection.commit()
    return result


# Read operation - R
def select_students():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM performance;")
        result = cursor.fetchall()
    connection.commit()
    return json.dumps(result, ensure_ascii=False)


def select_student(studentid):
    request = "SELECT * FROM performance WHERE studentid = ?;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(request, (studentid,))
        result = cursor.fetchall()
    connection.commit()
    obj = json.dumps(result, ensure_ascii=False)
    if obj == "null" or obj == "[]":
        pass
    else:
        return obj


# Update operation - U
def update_student(studentid, lecture_visits=None, practice_visits=None, practice=None):
    args = {}
    if not (lecture_visits is None):
        args["lecture_visits"] = lecture_visits
    if not (practice_visits is None):
        args["practice_visits"] = practice_visits
    if not (practice is None):
        args["practice"] = practice
    if len(args) == 0:
        return False
    reqargs = ' = ?, '.join(args.keys()) + " = ?"
    request = f"UPDATE performance SET {reqargs} WHERE studentid = ?;"
    with closing(connection.cursor()) as cursor:
        result = cursor.execute(request, (*args.values(), studentid))
        result = result.fetchone() is not None
    connection.commit()
    return result


# Delete operation - D
def delete_student(studentid):
    with closing(connection.cursor()) as cursor:
        result = cursor.execute("DELETE FROM performance WHERE studentid = ?;", (studentid,))
        result = result.fetchone() is not None
    connection.commit()
    return result
