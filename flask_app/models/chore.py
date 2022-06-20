from ast import Num
from flask_app.config.mysqlconnections import MySQLConnection, connectToMySQL
from flask import flash 
from flask_app.models import user 

class Chore:
    db = "chores_schema"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.job = db_data['job']
        self.location = db_data['location']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.job_taker_id = db_data['job_taker_id']
        self.user = None


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM chores LEFT join users ON user_id = users.id WHERE chores.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        chore = cls(results[0])
        user_data = {
                "id": results[0]["users.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["created_at"],
                "updated_at": results[0]["updated_at"]
            }
        chore.user = user.User(user_data)
        return chore

    @classmethod 
    def save(cls, data):
        query = "INSERT INTO chores(job, location, description, user_id) VALUES (%(job)s, %(location)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM chores LEFT join users ON user_id = users.id;" 
        results = connectToMySQL('chores_schema').query_db(query)
        chores = []
        for row in results:
            chore = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at": row["created_at"],
                "updated_at":row["updated_at"]
            }
            chore.user= user.User(user_data)
            chores.append( chore )
        return chores 

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM chores WHERE id= %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def update(cls, data):
        query = "UPDATE chores SET job = %(job)s, location = %(location)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)







    @classmethod
    def assign_job(cls, data):
        query = "UPDATE chores SET job_taker_id = %(job_taker_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)








    @staticmethod
    def validate_chore(chore):
        is_valid = True
        if len(chore['job']) < 1:
            is_valid = False
            flash("sorry, field cannot be blank")
        
        if len(chore['location']) < 1:
            is_valid = False
            flash("sorry, field cannont be left blank")
        
        if len(chore['description']) < 1:
            is_valid = False
            flash("sorry, field cannont be left blank")
        return is_valid
