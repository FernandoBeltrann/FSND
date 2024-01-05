from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from sqlalchemy import Delete


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/CRUD_todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean(), default = False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

    
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    todos = db.relationship('Todo', backref='list', cascade='all, delete-orphan' , lazy=True)

    def __repr__(self):
        return f'<Todo {self.id} {self.name}>'
        
with app.app_context(): 
    db.create_all()

@app.route('/todos/create/', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description'] 
        list_id = request.get_json()['list_id'] 
        todo = Todo(description=description, completed = False, list_id = list_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (500)
    if not error:
        return jsonify(body)
    
    
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        #print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect('/')

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
                           todolists= TodoList.query.all(),
                           lists=TodoList.query.order_by('id').all(),
                           active_list=TodoList.query.get(list_id),
                           todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
    first_displayed_list_id = TodoList.query.first().id
    return redirect(url_for('get_list_todos', list_id=first_displayed_list_id))



@app.route('/lists/create/', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        list_description = request.get_json()['list_description'] 
        list = TodoList(name=list_description)
        db.session.add(list)
        db.session.commit()
        body['id'] = list.id
        body['description'] = list.name
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (500)
    if not error:
        return jsonify(body)
    
@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)

        db.session.delete(list)

        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})

@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    try:
        completed = request.get_json()['completed']

        list = TodoList.query.get(list_id)

        for todo in list.todos:
            todo.completed = completed

        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect('/')

#--------------------Many to Many-----------------------

order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(), nullable=False)
  products = db.relationship('Product', secondary=order_items,
      backref=db.backref('orders', lazy=True))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

#-------------------------------------------------------