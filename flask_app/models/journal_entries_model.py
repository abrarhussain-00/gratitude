from flask import flash
from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model

mysql_db = "gratitude"


class Entry:
    def __init__(self, data):
        self.id = data['id']
        self.entry = data['entry']
        self.motivational_quote = data['motivational_quote']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.date = data['date']
        self.user_id = data['user_id']

# ---------- GET ALL ----------
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM journal_entries
        JOIN users ON users.id = journal_entries.user_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_journal_entries = []
        if results:
            for row in results:
                this_journal_entry = cls(row)
                user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "confirm_password": row['confirm_password'],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
                }
                this_user = users_model.User(user_data)
                this_journal_entry.poster = this_user
                all_journal_entries.append(this_journal_entry)
            return all_journal_entries
        return []

# ---------- GET ONE ----------
    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM journal_entries
        JOIN users ON users.id = journal_entries.user_id
        WHERE journal_entries.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        this_entry = cls(results[0])
        if results:
            for row in results: 
                user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
                }
                this_user = users_model.User(user_data)
                this_entry.poster = this_user
            return this_entry
        return False

# ---------- GET ALL BY USER ID ----------
    @classmethod
    def get_all_by_user_id(cls, data):
        query = """
        SELECT * FROM journal_entries
        WHERE journal_entries.user_id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        all_entries = []
        for row in results:
            all_entries.append(cls(row))
        return all_entries


# ---------- GET ONE BY DATE ----------
    @classmethod
    def get_one_by_date(cls, data):
        query = """
        SELECT * FROM journal_entries
        JOIN users ON users.id = journal_entries.user_id
        WHERE journal_entries.date = %(date)s AND journal_entries.user_id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        # print(data)
        print(results)
        
        if results:
            this_entry = cls(results[0])
            for row in results: 
                user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
                }
                this_user = users_model.User(user_data)
                this_entry.poster = this_user
            return this_entry
        else:
            return False


# ---------- CREATE ENTRY ----------
    @classmethod
    def create_entry(cls, data):
        query = """
        INSERT INTO journal_entries (entry, motivational_quote, user_id, date)
        VALUES (%(entry)s,%(motivational_quote)s,%(user_id)s, %(date)s);
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        return results

# ---------- EDIT ENTRY ----------
    @classmethod
    def edit_entry(cls, data):
        query = """
        UPDATE journal_entries
        SET entry = %(entry)s, 
            motivational_quote = %(motivational_quote)s, 
            updated_at = NOW() 
        WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if not results:
            return False
        return results

# ---------- DELETE Sight ----------
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM journal_entries
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# ---------- VALIDATION ----------
    @staticmethod
    def entry_validate(data):
        is_valid = True

        if len(data['entry']) < 5:
            is_valid =  False
            flash(f"Please enter a longer entry!")
        return is_valid
