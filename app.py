from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure your RDS database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:yourpassword@<RDS-ENDPOINT>/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Route to display all tasks
@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        new_task = Todo(task=task)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
