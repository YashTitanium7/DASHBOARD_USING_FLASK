from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect
from datetime import datetime
from os import system, startfile

system("clear")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///titaniumDatabase.db"
db = SQLAlchemy(app)

class Todo(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  desc = db.Column(db.String(500), nullable=False)
  date = db.Column(db.DateTime, default=datetime.utcnow())

  def __repr__(self) -> str:
    return f"{self.sno} - {self.title}"

class Workspace(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String(500), nullable=False)

# ==========Your Dashboard==========
@app.route('/')
def dashboard():
  return render_template('index.html')

# ==========Your Workspaces==========
@app.route('/Workspaces/', methods=['GET', 'POST'])
def workspaces():
  if request.method == 'POST':
    file = request.form['filePath']
    print(file)
    workspace = Workspace(path=file)
    db.session.add(workspace)
    db.session.commit()
  allWorkspaces = Workspace.query.all()
  return render_template('workspaces.html', list=allWorkspaces)

# ==========Your Projects==========
@app.route('/Projects')
def projects():
  return render_template('projects.html')

# ==========Your Tasks==========
@app.route('/tasks/', methods=['GET', 'POST'])
def tasks():
  if request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    todo = Todo(title=title, desc=description)
    db.session.add(todo)
    db.session.commit()
  allTodos = Todo.query.all()
  return render_template('tasks.html', allTodos=allTodos)

@app.route('/tasks/show')
def show():
  allTodos = Todo.query.all()
  print(allTodos)
  return "This is show page"

@app.route('/tasks/update/<int:sno>')
def update():
  return "update page"

@app.route('/tasks/delete/<int:sno>')
def delete(sno):
  todo = Todo.query.filter_by(sno=sno).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect("/tasks")

if __name__ == '__main__':
  app.run(debug=True)