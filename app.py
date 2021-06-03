from datetime import datetime
from typing import Text
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,  nullable=False)
    decs = db.Column(db.String,  nullable=False)
    dat = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.srno}-{self.title}"



@app.route("/",methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        decs=request.form['decs']
        todo=Todo(title=title,decs=decs)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()   
    return render_template('index.html',allTodo=allTodo)

@app.route("/update/<int:srno>",methods=["GET","POST"])
def update(srno):
    if request.method=="POST":
        title=request.form['title']
        decs=request.form['decs']
        todo=Todo.query.filter_by(srno=srno).first()
        todo.title=title
        todo.decs=decs
        db.session.add(todo) 
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(srno=srno).first()   
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:srno>")
def delete(srno):
    todo=Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True,port=8000)


