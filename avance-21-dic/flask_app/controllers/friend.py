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
@app.route('/login' , methods=['POST'])
def login():
    user = Friend.get_by_email(request.form)
    if not user:
        flash("Invalid email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.passwd, request.form['password']):
        flash("Invalid password", "login")
        return redirect('/')
    session['id_user'] = user.id
    return redirect('/dashboard')
#renderizar formulario para editar datos
@app.route('/edit')
def update_form():
    id = session['id_user']
    data = {
        'id_usuario': id
    }

    return render_template('edit.html', usuario = Friend.get_by_id(data))

@app.route('/update/<int:id_usuario>', methods=['POST'])
def update_user(id_usuario):
    id_usuario = session['id_user']
    if 'id_user' in session:
        data = {
            'id_usuario' : id_usuario,
            'nombre' : request.form['first_name'],
            'apellido': request.form['last_name'],
            'correo' : request.form['email']
        }
        print(data)
        Friend.update(data)
        return redirect('/edit')


@app.route('/dashboard')
def dashboard():
    data = {
        'id_usuario' : session['id_user']
    }
    return render_template('dashboard.html',
                            usuario = Friend.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')