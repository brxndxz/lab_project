from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Leukocyte_form:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.lymphocytes = data["lymphocytes"]
        self.neutrophils = data["neutrophils"]
        self.w_blood_cells = data["w_blood_cells"]
        self.monocytes = data["monocytes"]
        self.eosinophils = data["eosinophils"]
        self.basophils = data["basophils"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    #SAVE
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO leukocyte_formula (lymphocytes, neutrophils, w_blood_cells, monocytes, eosinophils, basophils, created_at, updated_at, user_id, category_id) VALUES (%(lymphocytes)s, %(neutrophils)s, %(w_blood_cells)s, %(monocytes)s, %(eosinophils)s, %(basophils)s NOW(), NOW(), %(user_id)s, 1);"
        return connectToMySQL('lab_bd').query_db( query, data )
    
    @classmethod
    def get_all(cls):
        results_instances = []
        query = "SELECT * FROM leukocyte_formula JOIN users ON leukocyte_formula.user_id = users.id;"
        results = connectToMySQL("lab_bd").query_db(query)

        for result in results:
            instance = cls(result)
            instance.user = user.User(result)
            results_instances.append(instance)
        return results_instances

    @classmethod
    def get(cls, id ):

        query="SELECT * FROM leukocyte_formula JOIN users ON user_id = users.id WHERE leukocyte_formula.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL('lab_bd').query_db(query, data)

        if results:
            instance = cls(results[0])
            instance.user = user.User(results[0])
            return instance
        return None
    
    def delete(self):
        query = "DELETE FROM leukocyte_formula WHERE id = %(id)s;"
        data = {'id': self.id}
        connectToMySQL('lab_bd').query_db(query, data)
        return True
    
    def update(self):
        query = """UPDATE leukocyte_formula SET 
                lymphocytes = %(lymphocytes)s, neutrophils =  %(neutrophils)s, 
                w_blood_cells =  %(w_blood_cells)s, monocytes =  %(monocytes)s,
                eosinophils =  %(eosinophils)s, basophils =  %(basophils)s,
                updated_at = NOW() WHERE id = %(id)s"""
        data = {
            'id': self.id,
            'lymphocytes': self.lymphocytes,
            'neutrophils': self.neutrophils,
            'w_blood_cells': self.w_blood_cells,
            'monocytes': self.monocytes,
            'eosinophils': self.eosinophils,
            'basophils': self.basophils
        }
        connectToMySQL('lab_bd').query_db( query, data )
        return True