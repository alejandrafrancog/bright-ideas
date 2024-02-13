from flask import flash,session
from ideas_app.config.mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  
db_name ="users"
class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.alias = data['alias']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def getId(cls,data):
        user_id = session.get("id")
        print(f"\n\nDATA:{data}\n\n")
        query = f"select * from users where id = %(id)s;"
        print(query)
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        if len(result) > 0:
            print("\nGET ID RESULT: ",result)
            return cls(result[0])
        else:
            return None
    @classmethod
    def getUserName(cls,data):
        query = f"select * from users where id = {data};"
        print(query)
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        if len(result) > 0:
            print("\nGET USER RESULT: ",result[0])
            return cls(result[0])
        else:
            return None
    @classmethod
    def getEmail(cls, email):
        query = "select * from users where email = %(email)s;"
        mysql = connectToMySQL(db_name)
        data = {
            'email': email
        }
        result = mysql.query_db(query, data)
        print(result)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def save(cls, data):
        query = "insert into users (name,alias,email, password) values "\
                "(%(name)s, %(alias)s, %(email)s, %(password)s);"
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        print(result)
        data_usuario = {'id': result}
        return cls.getId(data_usuario)
    
    @staticmethod
    def validate_user(usuario):
        is_valid = True 
        if len(usuario['name']) < 3:
            flash("El nombre debe tener al menos 3 caracteres")
            is_valid = False
        if len(usuario['alias']) < 3:
            flash("El alias debe tener al menos 3 caracteres")
            is_valid = False
        
        if not EMAIL_REGEX.match(usuario['email']): 
            flash("La dirección de email no es válida!")
            is_valid = False
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres")
            is_valid = False
        if usuario['confirm_password'] != usuario['password']:
            flash("Las contraseñas no son iguales")
            is_valid = False

        return is_valid 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db_name).query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        return users
    
    @classmethod
    def total_posts(cls,data):
        query = f"select count(user_id) from users left join ideas on users.id = ideas.user_id where user_id={data}";
        results = connectToMySQL(db_name).query_db(query)
        return results[0]['count(user_id)']