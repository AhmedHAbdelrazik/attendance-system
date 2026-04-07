import sqlite3
import pickle
from datetime import datetime

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    face_encoding BLOB NOT NULL
    )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        
    student_id  INTEGER NOT NULL,                 
    timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (student_id) REFERENCES Students (id) 
)
''')
conn.commit()
conn.close()


def add_student(name, face_encoding):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    face_encoding = sqlite3.Binary(pickle.dumps(face_encoding))
    cursor.execute('''
    INSERT INTO Students (name, face_encoding) VALUES (?, ?)
    ''', (name, face_encoding))
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return student_id

def get_all_students():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    rows = cursor.fetchall()
    conn.close()
    final_data = []
    for row in rows:
        unpacked_encoding = pickle.loads(row[2])
        final_data.append((row[0], row[1], unpacked_encoding))
    return final_data

def mark_attendance(student_id):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute('''
        SELECT * FROM Attendance 
        WHERE student_id = ? AND date(timestamp) = ?
    ''', (student_id, today))
    
    already_marked = cursor.fetchone()
    
    
    if not already_marked:
        cursor.execute('''
            INSERT INTO Attendance (student_id) VALUES (?)
        ''', (student_id,))
        conn.commit()
        conn.close()
        return True 
    
    conn.close()
    return False 


import pandas as pd

def get_attendance_report():
    conn = sqlite3.connect('attendance.db')
    query = '''
        SELECT Students.name, Attendance.timestamp 
        FROM Attendance 
        JOIN Students ON Attendance.student_id = Students.id
        ORDER BY Attendance.timestamp DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df    


def clear_attendance_records():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Attendance')
    
    conn.commit()
    conn.close()

