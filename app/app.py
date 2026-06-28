from flask import Flask, request
import os
import socket
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="devopsdb",
        user="devops",
        password="devops123"
    )

# Create table
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
    todos = cur.fetchall()
    cur.close()
    conn.close()

    html = f"""
    <h1>🐳 DevOps Practice App</h1>
    <p><strong>Host:</strong> {os.uname().nodename}</p>
    <hr>
    <h2>Yeni Tapşırıq Əlavə Et</h2>
    <form action="/add" method="post">
        <input type="text" name="task" placeholder="Tapşırıq yaz..." style="width:300px" required>
        <button type="submit">Əlavə et</button>
    </form>
    <hr>
    <h2>Tapşırıqlar Siyahısı ({len(todos)} ədəd)</h2>
    """

    if todos:
        html += "<ul>"
        for todo in todos:
            html += f"<li>✅ {todo['task']} <small>({todo['created_at']})</small></li>"
        html += "</ul>"
    else:
        html += "<p>Hələ heç bir tapşırıq yoxdur.</p>"

    return html

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        conn.commit()
        cur.close()
        conn.close()
    return "<h3>Task əlavə olundu! <a href='/'>← Geri</a></h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
