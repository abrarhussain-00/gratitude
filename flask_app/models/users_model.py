import re
from flask import flash
from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
# TO AVOID CIRCULAR IMPORT FOLLOW THIS SYNTAX
# from models import FILENAME
# when referencing the other model make sure you call on the other model as follows: FILENAME.CLASSNAME
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        # self.confirm_password = data['confirm_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ---------- GET ALL ----------
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        if results:
            for row in results:
                users.append(cls(row))
            return users
        return []

    # ---------- GET USER BY ID ----------
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []

    # ---------- GET USER BY EMAIL ----------
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []

    # ---------- REGISTER ----------
    @classmethod
    def register(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # ---------- VALIDATION ----------
    @staticmethod
    def register_validate(data):
        is_valid = True

        if len(data["first_name"]) < 2:
            is_valid =  False
            flash(f"First name must have at least 2 characters.", "register")

        if len(data["last_name"]) < 2:
            is_valid =  False
            flash(f"Last name must have at least 2 characters.", "register")

        if len(data["password"]) < 5:
            is_valid =  False
            flash(f"Password must be at least 5 characters.", "register")
        elif not data["password"] == data['confirm_pw']:
            is_valid =  False
            flash(f"Password must match.", "register")

        if len(data["email"]) < 1:
            is_valid = False
            flash(f"Email must be valid.", "register")
            return is_valid
        elif not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash(f"Email must be valid", "register")
            return is_valid
        else:
            email_check = {
                "email": data["email"]
        }
        potential_email = User.get_by_email(email_check)
        if potential_email:
            is_valid = False
            flash("Email already in use.", "register")

        return is_valid
