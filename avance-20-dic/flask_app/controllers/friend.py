from flask_app import app
from flask import request, render_template, redirect, session, flash

from ..models.friends import Friend
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if not Friend.validate_register(request.form):
        return redirect('/')
    data = {
        'nombre': request.form['first_name'],
        'apellido': request.form['last_name'],
        'email' : request.form['email'],
        'contrasenia' : bcrypt.generate_password_hash(request.form['passwd'])
    }
    id = Friend.save(data)
    session['id_user'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')