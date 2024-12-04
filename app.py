from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

# Configuration de la base de données
DB_HOST = "taskmanager-db.mysql.database.azure.com"
DB_USER = "ktarhami@mydbserver"
DB_PASSWORD = "Kawtar11@1"
DB_NAME = "taskmanager_db"

# Connexion à la base de données
def get_db_connection():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def index():
    # Affiche la liste des tâches
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, description, status, due_date FROM tasks")
    tasks = cursor.fetchall()
    db.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    # Ajout d'une nouvelle tâche
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)",
            (title, description, due_date)
        )
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Modifier une tâche existante
    db = get_db_connection()
    cursor = db.cursor()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = '1' if 'status' in request.form else '0'
        due_date = request.form['due_date']
        cursor.execute(
            "UPDATE tasks SET title=%s, description=%s, status=%s, due_date=%s WHERE id=%s",
            (title, description, status, due_date, task_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        task = cursor.fetchone()
        db.close()
        return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # Supprimer une tâche
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
