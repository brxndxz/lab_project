from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.hemogram import Hemogram
from flask_app.models.leukocyte_form import Leukocyte_form
from flask_app.models.user import User
import pymysql
db = pymysql.connect(host = 'localhost', user = 'root', password = '', db = 'lab_bd')

#EDIT 

@app.route("/hematological/<id>/edit")
def edit_hemogram(id):
    
    if "user" not in session:
        flash('Necesitas iniciar sesión.', 'error')
        return redirect("/")
    
    hemogram = Hemogram.get(id)

    return render_template("edit_hematological_analysis.html", hemogram = hemogram)

#PROCESS EDIT 

@app.route("/hematological/process_edit/<id>", methods=['POST'])
def process_edit_hemogram(id):
    hemogram = Hemogram.get(id)
    hemogram.hemoglobin = request.form['hemoglobin']
    hemogram.hematocric = request.form['hematocric']
    hemogram.r_blood_cells = request.form['r_blood_cells']
    is_valid, errors = hemogram.validate_hemogram(request.form)
    
    if not is_valid:
        for error in errors:
            print("ERROR: ", error)
            flash(error, "error")
        return redirect('/hematological/{}/edit'.format(id))
    
    hemogram.update()
    flash("Los cambios fueron guardados", "success")
    return redirect("/hematological/results")
#DELETE 
@app.route("/hematological/<id>/delete")
def delete(id):

    delete_hemogram = Hemogram.get(id)
    delete_hemogram.delete()

    flash("Hemograma eliminado", "success")
    return redirect("/hematological/results")

#HOME RENDER
@app.route("/home")
def show_home():
    if "user" not in session:
        flash('Necesitas iniciar sesión.', 'error')
        return redirect("/")
    user_in_session=User.get_id(session["user"])
    role_id = user_in_session.role_id
    print("ROLE IDDD", role_id)

    return render_template("home.html", role_id = role_id)

#SHOW FORM hematological
@app.route("/hematological/<id>/add")
def add_lab_test(id):

    user_in_session=User.get_id(session["user"])
    role_id = user_in_session.role_id
    if role_id == 1:
        user = User.get_id(id)
        return render_template("add_hem_labtest.html", user = user)
    elif role_id == 2:
        flash('No puedes acceder a esta página', 'error')
        return redirect("/home")
    
    if "user" not in session:
        flash('Necesitas iniciar sesión.', 'error')
        return redirect("/")


#PROCESS CREATE 
@app.route('/hemogram/create', methods=['POST'])
def process_hemogram():
    print("REQUEST FORM", request.form)

    r_blood_cells = request.form["r_blood_cells"] 
    hemoglobin = request.form["hemoglobin"]
    hematocric = request.form["hematocric"]
    user_id = request.form["user_id"]

    data = Hemogram.save({
        "r_blood_cells": r_blood_cells,
        "hemoglobin": hemoglobin,
        "hematocric": hematocric,
        "user_id": user_id
    })
    is_valid, errors = Hemogram.validate_hemogram(request.form)

    if not is_valid:
       for error in errors:
            print("ERROR: ", error)
            flash(error, "error")
            return redirect('/home')
       
    print("MIIIII DATAAAAAA", data)
    if data:
        flash("Análisis guardado exitosamente", "success")
    else:
        flash("Error.", "error")
    return redirect("/home")
#PROCESS LEUKOCYTE FORM
@app.route('/leukocyte_form/create', methods=['POST'])
def process_leukocyte_form():
    print("REQUEST FORM", request.form)

    w_blood_cells = request.form["w_blood_cells"] 
    lymphocytes = request.form["lymphocytes"]
    neutrophils = request.form["neutrophils"]
    monocytes = request.form["monocytes"]
    eosinophils = request.form["eosinophils"]
    basophils = request.form["basophils"]
    user_id = request.form["user_id"]

    data = Leukocyte_form.save({
        "w_blood_cells": w_blood_cells,
        "lymphocytes": lymphocytes,
        "neutrophils": neutrophils,
        "monocytes": monocytes,
        "eosinophils": eosinophils,
        "basophils": basophils,
        "user_id": user_id
    })
    print("MMMMIIIII DATAAAAAA", data)
    if data:
        flash("Análisis guardado exitosamente", "success")
    else:
        flash("Error.", "error")
    return redirect("/home")

    
    #is_valid, errors = Painting.validate_painting(request.form)

    #if not is_valid:
     #   for error in errors:
      #      print("ERROR: ", error)
       #     flash(error, "error")
        #return redirect('/paintings/new')

#SHOW RESULT
@app.route("/hematological/<id>/view")
def show_hematological(id):

    hemogram = Hemogram.get(id)

    if "user" not in session:
        flash('Necesitas iniciar sesión.', 'error')
        return redirect("/")
    
    return render_template("hematological_result.html", hemogram = hemogram)

@app.route('/hematological', methods = ['GET', 'POST'])
def show_to_add_hematological():
    if "user" not in session:
        flash('Necesitas iniciar sesión.', 'error')
        return redirect("/")
    
    if request.method == 'POST' and 'txtname' in request.form:
        name = request.form["txtname"]
        data = {"first_name": name}
        resultados = User.search(data)
    else:
        resultados = User.get_all()
    return render_template("search_to_add_hem.html", resultados = resultados)
#____________________________________________________________________________________________________
@app.route('/hematological/results', methods = ['GET', 'POST'])
def hematological():
    if request.method=='POST' and 'txtname' in request.form:
        print(request.form)
        name = request.form['txtname']
        data = {"first_name": name}
        resultados = Hemogram.search_hem(data)
    #sql = "SELECT * FROM hemograms WHERE created_at LIKE '%" + request.form['txtfecha'] + "%'"
    #sql = "SELECT * FROM hemograms JOIN users ON hemograms.user_id = users.id WHERE created_at LIKE '%" + request.form['txtfecha'] + "%'"
    #sql = "SELECT hemograms.*, users.column_name FROM hemograms JOIN users ON hemograms.user_id = users.user_id WHERE users.column_name LIKE %s"
    else:
        resultados = Hemogram.get_all()
    #sql = "SELECT * FROM hemograms JOIN users ON hemograms.user_id = users.id"
    #sql = "SELECT hemograms.*, users.firstn FROM hemograms JOIN users ON hemograms.user_id = users.id"
        print ("RESULTADOS  id 1", resultados)
    user_in_session=User.get_id(session["user"])
    role_id = user_in_session.role_id
    return render_template("show_hematologicals.html", resultados = resultados, role_id = role_id)

@app.route('/hematological/results/patient')
def show_results_patient():
    user_in_session=User.get_id(session["user"])
    user_id = user_in_session.id
    data = {"user_id": user_id}
    resultados = Hemogram.get_all_patient_results(data)
    print("GET ALL PATIENT RESULTS", resultados)
    return render_template("patients/show_all_results.html", resultados = resultados)