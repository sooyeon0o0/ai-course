from flask import Flask, render_template, request, redirect, url_for
import os
import sys

# app.py 파일이 위치한 디렉토리를 sys.path에 추가하여 database.py 등을 임포트할 수 있게 함
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from database import init_db, add_todo, get_all_todos, toggle_todo, delete_todo

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# 앱 시작 시 데이터베이스 초기화
with app.app_context():
    init_db()

@app.route('/')
def index():
    todos = get_all_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        add_todo(title)
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    toggle_todo(todo_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    delete_todo(todo_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
