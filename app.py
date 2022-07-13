from datetime import datetime
from operator import methodcaller
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id



@app.route('/', methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding the data to DB! Try again later'
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error trying to delete the record'

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if(request.method == 'POST'):
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error updating the records"
    else:
        return render_template('update.html', task=task_to_update)

if __name__=="__main__":
    app.run(debug=True)