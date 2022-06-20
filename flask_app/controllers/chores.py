from crypt import methods 
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.chore import Chore
from flask_app.models.user import User

@app.route('/create/chore', methods = ['POST'])
def create_chore():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Chore.validate_chore(request.form):
        return redirect('/add/chore')
    data ={
            "job": request.form["job"],
            "location": request.form["location"],
            "description": request.form["description"],
            "user_id": session["user_id"]
        }
    Chore.save(data)
    return redirect('/dashboard')

@app.route('/add/chore')
def add_chore():
    return render_template("add_chore.html")





@app.route('/job/taken/<int:id>')
def job_taken(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "job_taker_id" : session["user_id"],
        "id": id
    }
    Chore.assign_job(data)
    return redirect('/dashboard')






@app.route('/delete/chore/<int:id>')
def delete_chore(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id": id
    }
    Chore.delete(data)
    return redirect('/dashboard')

@app.route('/edit/chore/<int:id>')
def edit_chore(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data ={
        "id": id
    }
    user_data ={
        "id": session['user_id']
    }
    return render_template("edit_chore.html", chore = Chore.get_one(data), user = User.get_by_id(user_data))

@app.route('/update/chore/<int:id>', methods = ['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Chore.validate_chore(request.form):
        return redirect('/add/chore')
    data={
        "id" : id,
        "job": request.form['job'],
        "location": request.form['location'],
        "description": request.form['description'],
    }
    Chore.update(request.form)
    return redirect('/dashboard')

@app.route('/view/chore/<int:id>')
def view_chore(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        'id': id
    }
    user_data={
        "id": session['user_id']
    }
    return render_template("view_chore.html", chore = Chore.get_one(data), user = User.get_by_id(user_data))
