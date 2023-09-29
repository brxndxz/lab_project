from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Hemogram:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.hematocric = data["hematocric"]
        self.hemoglobin = data["hemoglobin"]
        self.r_blood_cells = data["r_blood_cells"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
    @staticmethod
    def validate_hemogram(user_form):
        is_valid = True 
        errors = []
        if not user_form['hematocric'].isnumeric():
            errors.append('Solo se permiten valores númericos')
            is_valid = False
        if not user_form['r_blood_cells'].isnumeric():
            errors.append('Solo se permiten valores númericos')
            is_valid = False
        if not user_form['hemoglobin'].isnumeric():
            errors.append('Solo se permiten valores númericos')
            is_valid = False
        return is_valid, errors
    #SAVE
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO hemograms (hematocric, hemoglobin, r_blood_cells, created_at, updated_at, user_id, category_id) VALUES (%(hematocric)s, %(hemoglobin)s, %(r_blood_cells)s, NOW(), NOW(), %(user_id)s, 1);"
        return connectToMySQL('lab_bd').query_db( query, data )
    
    @classmethod
    def get_all(cls):
        results_instances = []
        query = "SELECT * FROM hemograms JOIN users ON hemograms.user_id = users.id;"
        results = connectToMySQL("lab_bd").query_db(query)
        for result in results:
            instance = cls(result)
            instance.user = user.User(result)
            results_instances.append(instance)
        return results_instances

    @classmethod
    def get_hem(cls):
        results_instances = []

        query = "SELECT * FROM hemograms JOIN users ON hemograms.user_id = users.id;"
        results = connectToMySQL("lab_bd").query_db(query)

        for result in results:
            instance = cls(result)
            instance.user = user.User(result)
            results_instances.append(instance)
        return results_instances
    
    @classmethod
    def search_hem(cls, data):
        print("data search hem", data)
        instance_results = []
        
        query = "SELECT hemograms.*, users.first_name FROM hemograms JOIN users ON hemograms.user_id = users.id WHERE users.first_name LIKE %(first_name)s"
    
        results = connectToMySQL('lab_bd').query_db(query, data)
        for result in results:
            instancia = cls(result)
            instance_results.append(instancia)
        return instance_results
    @classmethod
    def get_all_patient_results(cls, data):
        print("data search hem", data)
        instance_results = []
        query = "SELECT hemograms.*, users.first_name FROM hemograms JOIN users ON hemograms.user_id = users.id WHERE hemograms.user_id = %(user_id)s"
        #query = "SELECT * FROM hemograms JOIN users ON hemograms.user_id = users.id WHERE hemograms.user_id = %(user_id)s"
        results = connectToMySQL('lab_bd').query_db(query, data)
        print ("RESULTS LABTESTS", results)
        for result in results:
            instancia = cls(result)
            instance_results.append(instancia)
        return instance_results
    
    @classmethod
    def get(cls, id ):

        query="SELECT * FROM hemograms JOIN users ON user_id = users.id WHERE hemograms.id = %(id)s;"
        
        data = {'id': id}
        results = connectToMySQL('lab_bd').query_db(query, data)

        if results:
            instance = cls(results[0])
            instance.user = user.User(results[0])
            return instance
        return None
    
    def delete(self):
        query = "DELETE FROM hemograms WHERE id = %(id)s;"
        data = {'id': self.id}
        connectToMySQL('lab_bd').query_db(query, data)
        return True
    
    def update(self):
        query = "UPDATE hemograms SET hemoglobin = %(hemoglobin)s, hematocric =  %(hematocric)s, r_blood_cells =  %(r_blood_cells)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'hemoglobin': self.hemoglobin,
            'hematocric': self.hematocric,
            'r_blood_cells': self.r_blood_cells
        }
        connectToMySQL('lab_bd').query_db( query, data )
        return True
    