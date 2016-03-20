from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from dateutil.parser import parse
from flask import json



app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)




class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(100))
    priority = db.Column(db.String(100))
    due = db.Column(db.Date)
    done = db.Column(db.Boolean)

    def __init__(self,task,priority,due,done):
        self.task = task
        self.priority = priority
        self.due = due
        self.done = done




query = db.session.query(Todo)





@app.route('/todo/<int:task_id>')
def index(task_id):
    return jsonify(greeting="<h1>Hello Task Id # {}</h1>".format(task_id))


@app.route('/todo', methods=['GET'])
def get_all_tasks():
    query = db.session.query(Todo)
    results = query.filter_by(done=False).all()
    reslist = []
    for row in results:
        reslist.append(dict(id=row.id, task=row.task, priority=row.priority, due=row.due.isoformat()))
        #end up with a list of dictionaires
    #print(reslist)
    return jsonify(tasklist=reslist)



@app.route('/todo/post', methods=['POST'])
def add_task():
    r = request.data.decode()
    d = json.loads(r)
    task = d['task']
    priority = d['priority']
    due = d['due']
    newtask = Todo(task,priority,parse(due).date(), False)
    #if newtask not in db.session.query():
    db.session.add(newtask)
    db.session.commit()
    return request.data



if __name__ == '__main__':
    app.run()
