from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models.painting import Painting
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.email = data["email"]
        self.first_name = data.get("first_name", "")
        self.last_name = data.get("last_name", "")
        self.age = data["age"]#agregué
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.role_id = data["role_id"]

    @staticmethod
    def validate_user(user_form):
        is_valid = True 
        errors = []
        #FIRST NAME
        if len(user_form['first_name']) < 2:
            errors.append("Name must be at least 2 characters.")
            is_valid = False
        if not user_form['first_name'].isalpha():
            errors.append("First name must be only alphabetic characters")
            is_valid = False
        #LAST NAME
        if len(user_form['last_name']) < 2 :
            errors.append("Last name must be at least 2 characters.")
            is_valid = False
        if not user_form['last_name'].isalpha():
            errors.append("Last name must be only alphabetic characters")
            is_valid = False
        #EMAIL
        if not EMAIL_REGEX.match(user_form['email']): 
            errors.append("Invalid email address!")
            is_valid = False
        #PASSWORD
        if len(user_form['password']) < 8:
            errors.append("Password must be at least 8 characters.")
            is_valid = False
        return is_valid, errors
    
    @classmethod 
    def save(cls, result ):
        query = "INSERT INTO users (first_name, last_name, email, age, password, role_id, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(age)s, %(password)s, 2, NOW(), NOW());"
        return connectToMySQL('lab_bd').query_db( query, result )
    
    @classmethod
    def get_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('lab_bd').query_db(query, data)
        
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_id(cls, id):
        data = {'id' : id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('lab_bd').query_db(query,data)
        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def update(self):
        query = "UPDATE hemograms SET first_name = %(first_name)s, last_name =  %(last_name)s, age =  %(age)s, email =  %(email)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email
        }
        print("DATA UPDATE", data)
        connectToMySQL('lab_bd').query_db( query, data )
        return True
    
    @classmethod
    def get_all(cls):
        instance_results = []
        query = "SELECT * FROM users"
        results = connectToMySQL('lab_bd').query_db(query)
        for resultado in results:
            instancia = cls(resultado)
            instance_results.append(instancia)
        return instance_results
  
    # MODEL function
    @classmethod
    def search(cls, data):
        tipo = type(data)
        print("DATA TYPE", tipo ) #DATA TYPE <class 'str'>
        instance_results = []
        #query = "SELECT * FROM users WHERE first_name LIKE %s ORDER BY id DESC"
        #results = connectToMySQL('lab_bd').query_db(query, (data + '%',))
        query = "SELECT * FROM users WHERE first_name LIKE %(first_name)s ORDER BY id DESC"
        results = connectToMySQL('lab_bd').query_db(query, data)
        print("RESULTADOS de mi query", results)
        for result in results:
            instancia = cls(result)
            instance_results.append(instancia)
        return instance_results