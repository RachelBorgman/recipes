from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt      
import re
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters.", 'register')
            is_valid = False
        if user['password'] != user['c_pw']:
            flash("Passwords do not match.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data, user):
        print(user.__dict__)
        is_valid = True
        if len(data['email']) < 3:
            flash("Login Email must be at least 3 characters.", 'login')
            is_valid = False
        if len(data['password']) < 3:
            flash("Login Password must be at least 3 characters.", 'login')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Login Invalid email address!", 'login')
            is_valid = False
        if bcrypt.check_password_hash(user.password, data['password']):
            flash("Passwords Don't Match", 'login')
            is_valid = False
        return is_valid
    
    @classmethod
    def new_email(cls, data):
        print(data)
        query = "SELECT email FROM user WHERE email = %(email)s"
        result = connectToMySQL('recipes').query_db(query, data)
        print(result)
        if len(result) == 0:
            return True
        # print(f"Email is: {cls(result[0])}")
        # flash('Already Registered. Please Log in.')
        return False
    
    @classmethod
    def get_by_email(cls, data):
        print(data)
        query = "SELECT * FROM user WHERE email = %(email)s"
        result = connectToMySQL('recipes').query_db(query, data)
        if result is None:
            flash('Please Register First')
            return False
        return cls(result[0])
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def get_by_id(cls, id):
        query = """
                SELECT * FROM user
                WHERE id = %(id)s;
        """
        result = connectToMySQL('recipes').query_db(query, id)
        print("getbyid result:")
        print(result)
        return cls(result[0])


