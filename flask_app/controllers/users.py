from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import pymysql
db = pymysql.connect(host = 'localhost', user = 'root', password = '', db = 'lab_bd')

@app.route("/")
def show_index():
    return render_template("auth/index.html")

@app.route("/register")
def show_register():
    return render_template("register_patients.html")

@app.route('/register/user', methods=['POST'])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    age = request.form["age"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    data = {"email": email}
    user = User.get_email(data)

    if user:
        flash("The user already exists.", "error")
        return redirect("/home")

    if password != confirm_password:
        flash("Passwords don't match.", "warning")
        return redirect('/home')
    
    is_valid, errors = User.validate_user(request.form)

    if not is_valid:
       for error in errors:
            print("ERROR: ", error)
            flash(error, "error")
            return redirect('/home')

    password_hash = bcrypt.generate_password_hash(password)
    print(password_hash)

    result = User.save({
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "email": email,
        "password": password_hash
    })
    
    if result:
        flash("Registered Successfully.", "success")
    else:
        flash("Error, no se pudo registrar", "error")
    return redirect("/register")

#LOG IN
@app.route("/login", methods=["POST"])
def login():
   
    email = request.form["email"]
    password = request.form["password"]

    data = {"email": email}
    user = User.get_email(data)

    if not user:
        flash("User or password is incorrect.", "error")
        return redirect("/")

    check_password = bcrypt.check_password_hash(user.password, password)
    role_id = user.role_id

    if check_password:
        session["user"] = user.id
        flash("You are logged in.", "info")
        return redirect('/home')
    else:
        flash("Hubo un error al iniciar sesión.", "error")
        return redirect('/')
#LOG OUT
@app.route("/logout/")
def logout():
    
    if "user" not in session:
        return redirect('/')

    session.clear()
    flash("Cerraste sesión.", "info")
    return redirect('/')

#EDIT 
#EDIT USER
@app.route("/user/<id>/edit")
def edit_(id):
    
    if "user" not in session:
        flash('Necesitas iniciar sesión.', 'error')
        return redirect("/")
    
    user = User.get_id(id)

    return render_template("edit_user.html", user = user)

#PROCESS EDIT USER

@app.route("/user/edit/<id>", methods=['POST'])
def process_edit_user(id):
    user = User.get_id(id)
    print("MI ID USERRRRR: ", user)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.email = request.form['email']
    user.age = request.form['age']
    user.update()
    print("MI FUNCION UPDATE: ", user)

    return redirect("/show/patients")

# CONTROLLER function
@app.route('/show/patients', methods=['GET', 'POST'])
def show_patients():
    if request.method == 'POST' and 'txtname' in request.form:
        name = request.form["txtname"]
        data = {"first_name": name}
        users = User.search(data)
    else:
        users = User.get_all()
    return render_template("search_patients.html", users=users)
 #data = {"first_name": "%" + name + "%"}