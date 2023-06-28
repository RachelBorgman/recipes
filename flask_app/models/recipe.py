from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models.user import User
# import re

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.date_cooked = data['date_cooked']
        self.user = data['user']
        # self.creator = None

    @classmethod
    def save(cls,data):
        print("in save")
        if not cls.validate_recipe(data):
            return False
        print("Data passed into create METHOD:", data)
        query = "INSERT INTO recipe (name, under, description, instructions, date_cooked, user_id) VALUES (%(name)s, %(under)s, %(description)s, %(instructions)s, %(date_cooked)s, %(user_id)s);"
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def validate_recipe(cls,data):
        print("in validate")
        is_valid = True
        if len(data['name'])<3:
            print("invalid")
            flash("Name must contain at least three characters.", 'recipes')
            is_valid = False
        if len(data['description'])<3:
            print("invalid")
            flash("Description must contain at least three characters.",'recipes')
            is_valid = False
        if len(data['instructions'])<3:
            print("invalid")
            flash("Instructions must contain at least three characters.",'recipes')
            is_valid = False
        if len(data['date_cooked'])<1:
            print("invalid")
            flash("Date Cooked can't be left blank",'recipes')
            is_valid = False
        print("valid")
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = """
        SELECT recipe.id, recipe.name, recipe.description, recipe.instructions, recipe.date_cooked, recipe.under, recipe.created_at, recipe.updated_at, user.id AS `user_id`, user.first_name, user.last_name, user.email, user.created_at, user.updated_at FROM recipe
        JOIN user ON recipe.user_id = user.id;
        """
        results = connectToMySQL('recipes').query_db(query)
        print(results)
        all_recipes = []
        for row in results:
            recipe_author = User({
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "created_at": row["user.created_at"],
                "updated_at": row["user.updated_at"],
                "password": ""
            })
            new_recipe = Recipe({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "instructions": row["instructions"],
                "date_cooked": row["date_cooked"],
                "under": 'no' if row["under"] == 0 else 'yes',
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user": recipe_author
            })
            all_recipes.append(new_recipe)
        return all_recipes
    
    @classmethod
    def get_by_id(cls, recipe_id):
        query = """
                SELECT * FROM recipe
                WHERE id = %(id)s;
        """
        data = {
            "id":recipe_id
        }
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            recipe = result[0]
            return recipe
        return False
    
    @classmethod
    def get_one(cls, data):
        print(data)
        query = """
                SELECT recipe.id, recipe.name, recipe.description, recipe.instructions, recipe.date_cooked, recipe.under, recipe.created_at, recipe.updated_at, user.id AS `user_id`, user.first_name, user.last_name, user.email, user.created_at, user.updated_at FROM recipe
                JOIN user ON recipe.user_id = user.id
                WHERE recipe.id = %(id)s;
        """
        results = connectToMySQL('recipes').query_db(query, {"id": data})
        # print(results)
        if not results:
            return False
        for row in results:
            creator = User({
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "created_at": row["user.created_at"],
                "updated_at": row["user.updated_at"],
                "password": ""
            })
            recipe = Recipe({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "instructions": row["instructions"],
                "date_cooked": row["date_cooked"],
                "under": 'no' if row["under"] == 0 else 'yes',
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user": creator
            })
        results = results[0]
        # recipe.creator =  creator
        return recipe
    
    @classmethod
    def update(cls,recipe):
        query = """
            UPDATE recipe
            SET name = %(name)s, under = %(under)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s, date_cooked = %(date_cooked)s
            WHERE id = %(id)s;
        """
        results = connectToMySQL('recipes').query_db(query, recipe)
        return results
    
    @classmethod
    def delete(cls, recipe_id):
        query = "DELETE FROM recipe WHERE id = %(id)s;"
        connectToMySQL('recipes').query_db(query, {"id":recipe_id})
        return recipe_id