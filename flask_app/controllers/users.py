from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register/user', methods=['POST'])
def register():
    if not User.new_email(request.form):
        print("not new")
        return redirect('/')
    if not User.validate(request.form):
        print("not valid")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    id = User.save(data)
    print(id)
    user = User.get_by_id({"id": id})
    session['id'] = id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    return redirect("/recipes")

@app.route('/login/user', methods=["POST"])
def login_user():
    # pw_hash = bcrypt.generate_password_hash(request.form['login_password'])
    data = {
        'email': request.form['login_email'],
        'password': request.form['login_password']
    }
    user = User.get_by_email(data)
    if not User.validate_login(data, user):
        return redirect('/')
    print(user)
    session['id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    
    return redirect('/recipes')

@app.route("/recipes")
def recipes():
    if 'id' in session:
        data = {
            'id': session['id']
        }
    all_recipes = Recipe.get_all()
    current_user = User.get_by_id(data)
    print(current_user)
    return render_template("recipes.html", user=current_user, all_recipes=all_recipes)

@app.route("/logout")
def logout():
    session.clear()
    session['id'] = None
    print("session cleared")
    return redirect("/")
