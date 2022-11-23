import sqlite3
from contextlib import closing
import json

connection = sqlite3.connect('students.db', check_same_thread=False)


# Create (insert) operation - C
def insert_student(studentid, fname, sname, lname, groupid):
    with closing(connection.cursor()) as cursor:
        result = cursor.execute(
            f"INSERT INTO students(studentid, fname, sname, lname, groupid) VALUES (?, ?, ?, ?, ?);",
            (studentid, fname, sname, lname, groupid))
        result = result.fetchone() is not None
    connection.commit()
    return result


# Read operation - R
def select_students():
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM students;")
        result = cursor.fetchall()
    connection.commit()
    return json.dumps(result, ensure_ascii=False)


def select_student(studentid=None, fname=None, sname=None, lname=None, groupid=None):
    args = {}
    if not (studentid is None):
        args["studentid"] = studentid
    if not (fname is None):
        args["fname"] = fname
    if not (sname is None):
        args["sname"] = sname
    if not (lname is None):
        args["lname"] = lname
    if not (groupid is None):
        args["groupid"] = groupid
    if len(args) == 0:
        return select_students()
    reqargs = ' = ? AND '.join(args.keys()) + " = ?"
    request = "SELECT * FROM students WHERE " + reqargs + ";"
    with closing(connection.cursor()) as cursor:
        cursor.execute(request, list(args.values()))
        result = cursor.fetchall()
    connection.commit()
    obj = json.dumps(result, ensure_ascii=False)
    if obj == "null" or obj == "[]":
        pass
    else:
        return obj


# Update operation - U
def update_student(studentid, fname=None, sname=None, lname=None, groupid=None):
    args = {}
    if not (fname is None):
        args["fname"] = fname
    if not (sname is None):
        args["sname"] = sname
    if not (lname is None):
        args["lname"] = lname
    if not (groupid is None):
        args["groupid"] = groupid
    if len(args) == 0:
        return False
    reqargs = ' = ?, '.join(args.keys()) + " = ?"
    request = f"UPDATE students SET {reqargs} WHERE studentid = ?;"
    with closing(connection.cursor()) as cursor:
        result = cursor.execute(request, (*args.values(), studentid))
        result = result.fetchone() is not None
    connection.commit()
    return result


# Delete operation - D
def delete_student(studentid):
    with closing(connection.cursor()) as cursor:
        result = cursor.execute("DELETE FROM students WHERE studentid = ?;", (studentid,))
        result = result.fetchone() is not None
    connection.commit()
    return result
