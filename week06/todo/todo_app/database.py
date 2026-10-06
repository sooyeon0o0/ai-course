import sqlite3
from datetime import datetime

DB_NAME = "todos.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """데이터베이스 및 테이블 초기화"""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def add_todo(title):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO todos (title) VALUES (?)', (title,))
        conn.commit()

def get_all_todos():
    with get_db_connection() as conn:
        # 미완료 항목을 상단에, 완료 항목을 하단에 배치하며 최신순 정렬
        todos = conn.execute('''
            SELECT * FROM todos 
            ORDER BY is_completed ASC, created_at DESC
        ''').fetchall()
        return todos

def toggle_todo(todo_id):
    with get_db_connection() as conn:
        conn.execute('UPDATE todos SET is_completed = 1 - is_completed WHERE id = ?', (todo_id,))
        conn.commit()

def delete_todo(todo_id):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
