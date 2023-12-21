from ..config.mysqlconnect import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Friend():
    db = 'friends'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.passwd = data['passwd']

    @classmethod
    def save(cls, data):
        query = 'insert into usuarios (first_name, last_name, email, passwd) values (%(nombre)s, %(apellido)s,%(email)s,%(contrasenia)s);'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = 'select * from usuarios where email = %(email)s;'
        results = connectToMySQL(Friend.db).query_db(query, user)
        if len(results) >= 1:
            flash("El mail ingresado ya existe", "register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Mail no válido!","register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("El nombre debe tener al menos 2 letras","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("El apellido debe tener al menos 3 letras","register")
            is_valid = False
        if len(user['passwd']) < 10:
            flash("La contraseña debe tener al menos 10 caracteres","register")
            is_valid = False
        if user['passwd'] != user['confirm-passwd']:
            flash("Las contraseñas no coinciden", "register")
        return is_valid