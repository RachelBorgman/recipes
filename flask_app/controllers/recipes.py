from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/add_recipe")
def render_add_recipe():
    return render_template("add_recipe.html")

@app.route("/add_recipe", methods=['POST'])
def add_recipe():
    print('under: ')
    print(request.form['under'])
    data = {
        'name' : request.form['name'],
        'under' : 0 if (request.form['under'] == 'no') else 1,
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'user_id' : session['id']
    }
    Recipe.save(data)
    return redirect("/recipes")

@app.route("/view_recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = Recipe.get_one(recipe_id)
    print("the recipe:")
    print(recipe)
    return render_template("view_recipe.html", recipe=recipe)

@app.route('/update_recipe/<int:recipe_id>')
def update(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    return render_template("update_recipe.html", recipe=recipe)

@app.route('/update_recipe/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    print(recipe_id)
    recipe = request.form
    print('under: ')
    print(request.form['under'])
    print(recipe)
    if not Recipe.validate_recipe(recipe):
        return redirect(f"/update_recipe/{recipe_id}")
    data = {
        'id': recipe_id,
        'name' : request.form['name'],
        'under' : 0 if (request.form['under'] == 'no') else 1,
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'user_id' : session['id']
    }
    # Recipe.save(data)
    Recipe.update(data)
    return redirect("/recipes")

@app.route("/delete/<int:recipe_id>")
def delete(recipe_id):
    Recipe.delete(recipe_id)
    return redirect("/recipes")
