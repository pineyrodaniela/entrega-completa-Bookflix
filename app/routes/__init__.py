from flask import render_template, request, session, escape, redirect, url_for, flash, send_from_directory
from app import app, db
from app.schemas import *
import datetime
from datetime import datetime
import os, random
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shutil, sys


@app.route("/listarCapitulosUser/<int:LibroId>")
def listarCapUser(LibroId):
    datetime_act = datetime.now()
    libro = Libros.query.filter_by(id=LibroId).first()
    capitulos = Capitulos.query.filter_by(lib_id=LibroId,).all()
    return render_template("listarCapitulosUser.html", capitulos = capitulos, libro = libro, datetime_act = datetime_act)

@app.route("/verPDF/<int:LibroId>")
def verPDF(LibroId):
    libro = Libros.query.filter_by(id=LibroId).first()
    capitulo = Capitulos.query.filter_by(lib_id=LibroId).first()
    pathF = capitulo.path + "\\" + capitulo.nomCap + "#toolbar=0"
    return render_template("vistaPDF.html", pathF = pathF)

@app.route("/verCapitulo/<int:LibroId>/<int:cap>")
def verCapitulo(LibroId,cap):
    libro = Libros.query.filter_by(id=LibroId).first()
    capitulo = Capitulos.query.filter_by(lib_id=LibroId,numCap = cap).first()
    pathF = capitulo.path + "\\" + capitulo.nomCap + "\\"
    return render_template("vistaPDF.html", pathF = pathF)

@app.route("/hora")
def hora():
    libro = Libros.query.filter_by(id=3).first()
    fecL =  "08-03-1997"
    datetime_act = datetime.now()
    datetime_object = datetime.strptime(fecL, '%d-%m-%Y' )

    return render_template("hora.html", fecL = datetime_object, datetime_act = datetime_act)

@app.route("/mostrarLibro/<int:n>")
def mostrarLibro(n):
    libro = Libros.query.get_or_404(n)
    capitulos = Capitulos.query.filter_by(lib_id=n).first()
    aut = Autores.query.filter_by(id = libro.autor_id).first()
    edit = Editoriales.query.filter_by(id = libro.editorial_id).first()
    gen = Generos.query.filter_by(id = libro.genero_id).first()
    datetime_act = datetime.now()
    if libro.tiene_trailer:
        trailerL = trailers.query.filter_by(libro_id=libro.id).first()
        return render_template("mostrarLibro.html", l =libro, c = capitulos, aut = aut, edit = edit, gen = gen, trailerL = trailerL, datetime_act = datetime_act)
    else:
        return render_template("mostrarLibro.html", l =libro, c = capitulos, aut = aut, edit = edit, gen = gen, datetime_act = datetime_act)

@app.route("/borrarLibro/<int:n>", methods= ["GET", "POST"])
def borrarLibro(n):
    libro = Libros.query.get_or_404(n)
    if libro is not None:
        libro.oculto = 1
        libro.capSubidosAct = 0
        Capitulos.query.filter_by(lib_id=n).delete()
        if (path.exists(app.config['UPLOAD_PDFs'] + "\\" + str(libro.id))):
            shutil.rmtree(app.config['UPLOAD_PDFs'] + "\\" + str(libro.id))

        db.session.commit()
        flash("Se eliminaron el libro y sus capitulos", "success")
    else:
        flash("Libro no eliminado", "error")
    return render_template("admin.html")



@app.route("/mostrarCapitulos/<int:n>", methods= ["GET", "POST"])
def mostrarCapitulos(n):
    libro = Libros.query.get_or_404(n)
    capitulo = Capitulos.query.filter_by(lib_id=n).all()
    return render_template("listarCapitulos.html", libro = libro, capitulo = capitulo, n = n)



@app.route("/borrarCapituloLibCompleto/<int:lib>/<int:cap>")
def borrarCapituloLibCompleto(lib,cap):
    libro = Libros.query.filter_by(id=lib).first()
    capitulo = Capitulos.query.filter_by(id=cap).first()
    if (path.exists(app.config['UPLOAD_PDFs'] + "\\" + str(libro.id))):
        shutil.rmtree(app.config['UPLOAD_PDFs'] + "\\" + str(libro.id))
        Capitulos.query.filter_by(id=cap).delete()
        libro.capSubidosAct = libro.capSubidosAct-1
        db.session.commit()
        flash("Capitulo eliminado", "success")
    else:
        flash("Capitulo no eliminado", "error")
    return render_template("admin.html")


@app.route("/borrarCapitulo/<int:lib>/<int:cap>")
def borrarCapitulo(lib,cap):
    libro = Libros.query.filter_by(id=lib).first()
    capitulo = Capitulos.query.filter_by(id=cap).first()
    if (path.exists(app.config['UPLOAD_PDFs'] + "\\" + str(libro.id) + "\\" + str(capitulo.numCap))):
        shutil.rmtree(app.config['UPLOAD_PDFs'] + "\\" + str(libro.id) + "\\" + str(capitulo.numCap))
        Capitulos.query.filter_by(id=cap).delete()
        libro.capSubidosAct = libro.capSubidosAct-1
        db.session.commit()
        flash("Capitulo eliminado", "success")
    else:
        flash("Capitulo no eliminado", "error")
    return render_template("admin.html")

@app.route("/modificarCapitulo/<int:lib>/<int:cap>", methods= ["GET", "POST"])
def modificarCapitulo(lib,cap):
    libro = Libros.query.filter_by(id=lib).first()
    capitulo = Capitulos.query.filter_by(id=cap).first()
    if request.method == "POST":
        fecV = request.form["fec_ven"]
        cantP = request.form["cantPags"]
        if (fecV == "") or (int(cantP) <= 0):
            flash("Campos Inválidos", "error")
            return render_template("admin.html")
        else:
            capitulo.fecha_vencimiento = request.form["fec_ven"]
            capitulo.cantidad_de_paginas = request.form["cantPags"]
            db.session.commit()
            flash("Capitulo modificado", "success")
            return render_template("admin.html")
    return render_template("modificarCapitulo.html", libro= libro, capitulo = capitulo)




UPLOAD_PDFs = os.path.abspath("./app/static/archivos/PDFs")
UPLOAD_PORTADAS = os.path.abspath("./imgs/Portadas/")
UPLOAD_FOLDER = os.path.abspath("./archivos/trailers")


app.config['UPLOAD_PDFs'] = UPLOAD_PDFs
app.config['UPLOAD_PORTADAS'] = UPLOAD_PORTADAS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(["pdf", "mp4", "avi", "mov", "flv"])
extensionesLibros = set(["pdf"])
extensionesPortadas = set(["jpg", "png", "jpeg", "bmp" ])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_file_port(filename):
    return '.' in filename and \
        filenape.rsplit('.', 1)[1] in extensionesPortadas

def allowed_file_lib(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensionesLibros

@app.route("/subirCapitulo/<int:n>", methods= ["GET", "POST"])
def subirCapitulo(n):
        libro = Libros.query.get_or_404(n)

        if request.method == "POST":
            if "PDF" not in request.files:
                return("el formulario no tiene un archivo")
            f = request.files["PDF"]
            if f.filename == "":
                flash ("no se seleccionó un archivo", "error")

            if f and allowed_file_lib(f.filename):
                num = libro.capSubidosAct+1
                direc = UPLOAD_PDFs + "\\" + str(libro.id) + "\\" + str(num)

                pathFile = "\static\\archivos\PDFs" + "\\" + str(libro.id) + "\\" + str(num)

                if path.exists(direc):
                    flash("Ya existe esa direccion", "error")
                else:
                    os.makedirs(direc)
                filename = secure_filename(f.filename)
                fecha = datetime.strptime(request.form["fec_ven"], '%d-%m-%Y' )
                nue_cap = Capitulos(nomCap= filename, lib_id= n, numCap= libro.capSubidosAct+1, fecha_vencimiento= fecha,
                                    cantidad_de_paginas= request.form["cantPags"], path= os.path.join(pathFile))

                libro.capSubidosAct = libro.capSubidosAct +1

                db.session.add(nue_cap)
                db.session.commit()
                filename = secure_filename(f.filename)
                f.save(os.path.join(direc, filename))
                flash("Capitulo subido", "success")
                return render_template("admin.html")
        return render_template("subirPDF.html")


@app.route("/subirLibroCompleto/<int:n>", methods=["GET", "POST"])
def subirLibroCompleto(n):
    libro = Libros.query.get_or_404(n)
    if libro.cantCapTotales > 1:
            return("No se puede subir un PDF completo en un libro por capitulos")
    if request.method == "POST":
        if "PDF" not in request.files:
            return("el formulario no tiene un archivo")
        f = request.files["PDF"]
        if f.filename == "":
            flash ("no se seleccionó un archivo", "error")

        if (f and (not allowed_file_lib(f.filename))):
            flash("Archivo ingresado no válido", "error")

        capitulo = Capitulos.query.filter_by(lib_id=n).first()
        if capitulo:
            flash("El libro ya habia sido agregado", "error")
        elif f and allowed_file_lib(f.filename):
            direc = UPLOAD_PDFs + "\\" + str(libro.id)
            pathFile = "\static\\archivos\PDFs" + "\\" + str(libro.id)
            if path.exists(direc):
                messages = "Ya existe esa carpeta"
                return render_template("admin.html", messages = messages)

            else:
                os.makedirs(direc)

            filename = secure_filename(f.filename)
            fecha = datetime.strptime(request.form["fec_ven"], '%d-%m-%Y' )
            nue_cap = Capitulos(nomCap= filename, lib_id= n, numCap= 1, fecha_vencimiento= fecha,
                                cantidad_de_paginas= request.form["cantPags"], path= os.path.join(pathFile))

            libro.capSubidosAct = libro.capSubidosAct +1

            db.session.add(nue_cap)
            db.session.commit()
            filename = secure_filename(f.filename)
            f.save(os.path.join(direc, filename))
            flash("Libro completo subido", "success")
            return render_template("admin.html")
    return render_template("subirPDF.html")


@app.route("/darDeAlta", methods= ["GET", "POST"])
def darDeAlta():

    if "tipoUser" in session:
        if session["tipoUser"] != 3:
            return render_template("index.html")
        else:

            if request.method == "POST":

                if "editorial" in request.form:
                    editRepe = Editoriales.query.filter_by(nomEditorial=request.form["editorial"]).first()
                    if editRepe:
                        flash("Ya existe esa editorial en la base de datos.", "error")

                    else:

                        nue_editorial = Editoriales(nomEditorial= request.form["editorial"])

                        db.session.add(nue_editorial)
                        db.session.commit()
                        flash("Editorial subida", "success")

                if "genero" in request.form:
                    genRepe = Generos.query.filter_by(nomGenero=request.form["genero"]).first()

                    if genRepe:
                        flash("Ya existe ese genero en la base de datos.", "error")

                    else:
                        nue_genero = Generos(nomGenero= request.form["genero"])
                        db.session.add(nue_genero)
                        db.session.commit()
                        flash("Genero subido", "success")

                if  "autor" in request.form:
                    autRepe = Autores.query.filter_by(nomAutor=request.form["autor"]).first()

                    if autRepe:
                        flash("Ya existe ese autor en la base de datos.", "error")

                    else:
                        nue_autor = Autores(nomAutor= request.form["autor"])
                        db.session.add(nue_autor)
                        db.session.commit()
                        flash("Autor subido", "success")

        return render_template("darDeAlta.html")


@app.route("/cargarLibro", methods= ["GET", "POST"])
def cargarLibro ():
    if "tipoUser" in session:
        if session["tipoUser"] != 3 or session["tipoUser"] == None:

            return render_template("index.html")
        else:
            allGeneros = Generos.query.all()
            allAutores = Autores.query.all()
            allEditoriales = Editoriales.query.all()
            if request.method == "POST":
                libroRepe = Libros.query.filter_by(ISBN=request.form["ISBN"], oculto=0).first()



                if libroRepe is not None:
                    flash("El ISBN ingresado ya se encuentra en la base de datos", "error")
                    return render_template("agregarlibro.html", allEditoriales = allEditoriales, allGeneros = allGeneros, allAutores= allAutores)

                nue_libro = Libros(titulo= request.form["titulo"], descripcion = request.form["descripcion"],
                ISBN = request.form["ISBN"] , editorial_id= request.form["editorial"],
                autor_id = request.form["autor"], genero_id= request.form["genero"],
                fecha_edicion= request.form["edicion"],cantCapTotales= request.form["cantCap"])

                db.session.add(nue_libro)
                db.session.commit()
                flash("Libro añadido", "success")
            return render_template("agregarlibro.html", allEditoriales = allEditoriales, allGeneros = allGeneros, allAutores= allAutores)
    else:
        return redirect(url_for("login"))

@app.route('/modificarLibro/<int:n>', methods= ["GET", "POST"])
def modificarLibro (n):
    if session["tipoUser"] != 3 or session["tipoUser"] == None:
        return render_template("index.html")
    else:
        libroMod = Libros.query.get_or_404(n) #traigo el libro de la DB con id n
        if request.method == "POST":
            libroRepe = Libros.query.filter_by(ISBN=request.form["ISBN"]).first()


            if ((libroRepe is not(None)) and (libroRepe.id == libroMod.id)):
                msj = ""
                des = request.form["descripcion"]
                ISBN =request.form["ISBN"]
                fecEd= request.form["edicion"]
                if ((des == "") or (not des)):
                    msj = msj + "- Descripcion vacía \n"

                if (fecEd == ""):
                    msj = msj + "- campo fecha vacío \n"

                if msj != "":
                    flash("Error al modificar libro:" + "\n" + msj, "error")
                    return render_template("admin.html")
                else:
                    libroMod.descripcion = request.form["descripcion"]
                    libroMod.ISBN =request.form["ISBN"]
                    libroMod.editorial_id= request.form["editorial"]
                    libroMod.autor_id = request.form["autor"]
                    libroMod.genero_id= request.form["genero"]
                    libroMod.fecha_edicion= request.form["edicion"]


                    flash("Libro actualizado", "success")
                    db.session.commit()
            else:
                ISBN =request.form["ISBN"]
                if ((ISBN == "") or (int(ISBN) <= 0)):
                    flash("El ISBN ingresado es nulo o menor a 1", "error")
                else:
                    flash("El ISBN ingresado ya existe en la base de datos", "error")

            return render_template('admin.html')

        else:
            allGeneros = Generos.query.all()
            allAutores = Autores.query.all()
            allEditoriales = Editoriales.query.all()
            return render_template("modificarLibro.html", libroMod = libroMod, allEditoriales = allEditoriales, allGeneros = allGeneros, allAutores= allAutores)




@app.route("/traerLibros")
def traerLibros():
    if "tipoUser" in session:
        if session["tipoUser"] != 3:
            return render_template("index.html")
        else:
            allLibros = Libros.query.filter_by(oculto=0).all()
            allAutores = Autores.query.all()
            return render_template("traerLibros.html", allLibros = allLibros, allAutores = allAutores)

@app.route("/librosPorCapitulo")
def porCapitulo():
    if "tipoUser" in session:
        if session["tipoUser"] != 3:
            return render_template("index.html")
        else:
            allLibros = Libros.query.filter_by(porCapitulo=1).all()
            allAutores = Autores.query.all()
            return render_template("traerLibros.html", allLibros = allLibros, allAutores = allAutores)


@app.route("/admin")
def admin():
    if "tipoUser" in session:
        if session["tipoUser"] != 3:
            return render_template("index.html")
        else:
            return render_template("admin.html")



@app.route("/signup")
def signup():
    if "usermail" in session:
        return redirect(url_for("index"))

    return render_template("signup.html")

@app.route("/signup/premium", methods=["GET", "POST"])
def signup_premium():
    if "usermail" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        # Chequear que el correo y el dni no esten ya registrados en la database
        todoOk = True

        correoRepe = Users.query.filter_by(correo=request.form["correo"]).first()
        dniRepe = Users.query.filter_by(dni_titular_tarjeta=request.form["titularTarj"]).first()

        if correoRepe or dniRepe:
            todoOk = False

        # Registra a un nuevo usuario en la base de datos
        if todoOk:
            new_user = Users( nombre=request.form["nombre"],
                              clave=request.form["password1"],
                              apellido=request.form["apellido"],
                              fecha_nac=request.form["nacimiento"],
                              correo=request.form["correo"],
                              dni_titular_tarjeta=request.form["titularTarj"],
                              tipo_tarjeta=request.form["tipos_tarj"],
                              num_tarjeta=request.form["numero_de_tarjeta"],
                              titular_tarjeta=request.form["nombre_titular_tarjeta"],
                              cvc=request.form["cvc_tarj"],
                              mes_venc=request.form["exMonth"],
                              anio_venc=request.form["exYear"],
                              tipo_de_usuario=2,
                              deleted_user="False")

            db.session.add(new_user)
            db.session.commit()

            new_perfil = Perfiles( usuario_id=new_user.id,
                                   nombre_perfil=new_user.nombre,
                                   imagen_de_perfil="../static/imgs/avatar-default.png",
                                   perfil_borrado="False")

            db.session.add(new_perfil)
            db.session.commit()

            flash("Te has registrado exitosamente", "success")

            return redirect(url_for("login"))
        else:
            if correoRepe:
                flash("Ya existe una cuenta asociada al correo electrónico ingresado. Vuelve a intentarlo.", "error")
            if dniRepe:
                flash("Ya existe una cuenta asociada al DNI ingresado. Vuelve a intentarlo.", "error")

    return render_template("signup-premium.html")


@app.route("/signup/standard", methods=["GET", "POST"])
def signup_standard():
    if "usermail" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        # Chequear que el correo y el dni no esten ya registrados en la database
        todoOk = True

        correoRepe = Users.query.filter_by(correo=request.form["correo"]).first()
        dniRepe = Users.query.filter_by(dni_titular_tarjeta=request.form["titularTarj"]).first()

        if correoRepe or dniRepe:
            todoOk = False

        # Registra a un nuevo usuario en la base de datos
        if todoOk:
            new_user = Users( nombre=request.form["nombre"],
                              clave=request.form["password1"],
                              apellido=request.form["apellido"],
                              fecha_nac=request.form["nacimiento"],
                              correo=request.form["correo"],
                              dni_titular_tarjeta=request.form["titularTarj"],
                              tipo_tarjeta=request.form["tipos_tarj"],
                              num_tarjeta=request.form["numero_de_tarjeta"],
                              titular_tarjeta=request.form["nombre_titular_tarjeta"],
                              cvc=request.form["cvc_tarj"],
                              mes_venc=request.form["exMonth"],
                              anio_venc=request.form["exYear"],
                              tipo_de_usuario=1,
                              deleted_user="False")

            db.session.add(new_user)
            db.session.commit()

            new_perfil = Perfiles( usuario_id=new_user.id,
                                   nombre_perfil=new_user.nombre,
                                   imagen_de_perfil="../static/imgs/avatar-default.png",
                                   perfil_borrado="False")

            db.session.add(new_perfil)
            db.session.commit()

            flash("Te has registrado exitosamente", "success")

            return redirect(url_for("login"))
        else:
            if correoRepe:
                flash("Ya existe una cuenta asociada al correo electrónico ingresado. Vuelve a intentarlo.", "error")
            if dniRepe:
                flash("Ya existe una cuenta asociada al DNI ingresado. Vuelve a intentarlo.", "error")

    return render_template("signup-standard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "usermail" in session:
        return render_template("index.html")

    if request.method == "POST":
        user = Users.query.filter_by(correo=request.form["correo_login"]).first()

        if user and (user.deleted_user=="True"):
            flash("No es posible iniciar sesión ya que esta cuenta de usuario ha sido borrada", "error")
            return render_template("login.html")

        if user and (user.clave == request.form["password_login"]):
            session["usermail"] = user.correo
            session["tipoUser"] = user.tipo_de_usuario
            user.datetime_acceso = datetime.now()
            db.session.commit()

            if (user.tipo_de_usuario == 3):
                return redirect(url_for("admin"))
            else:
                flash ("Has iniciado sesión. Bienvenido de nuevo!", "success_login")
                return redirect(url_for("index"))
        flash("El correo o la contraseña ingresados son inválidos, revisa e intenta de nuevo.", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    if "usermail" in session:
        session.pop("usermail", None) # Cierra la sesión
        session.pop("tipoUser", None)
        flash ("Ha cerrado la sesión con éxito.", "success_logout")
        return redirect(url_for("index"))

    else:
        flash("Debes iniciar sesion primero", "error")
        return redirect(url_for("login"))


#ruta raiz
@app.route("/")
def index():
    if "usermail" in session:
        libros = Libros.query.filter_by(oculto=0).all()
        return render_template("vistaUserRegistrado.html", libros=libros)
    else:
        libro = Libros.query.order_by(Libros.id).all()
        a = random.sample(libro, 5)
        return render_template("index.html", a=a)
#######################################

################ Sesiones ##############

@app.route("/acc")
def account():
    if "usermail" in session:
        elmail = session["usermail"]
        us = Users.query.filter_by(correo=elmail).first()
        infoDeAcceso = us.datetime_acceso
        return render_template("account.html", infoDeAcceso=infoDeAcceso)

    flash("Debes loguearte primero para acceder a la sección 'Ver Cuenta'", "error")
    return redirect(url_for("login"))


@app.route("/delete-account")
def delete_acc():
    if "usermail" in session:
        return render_template("delete-account.html")

    flash("Debes loguearte primero para acceder a esta seccion.", "error")
    return redirect(url_for("login"))

@app.route("/deleting")
def borrar_def():
    if "usermail" in session:
        usuario_a_borrar = session["usermail"] #se guarda el correo del usuario que está logueado

        user = Users.query.filter_by(correo=usuario_a_borrar).first() #obtiene el usuario a borrar

        user.deleted_user = "True" # Marca como True al Usuario Borrado

        db.session.commit() # hace efectivo los cambios

        session.pop("usermail", None) # Cierra la sesión
        session.pop("tipoUser", None)

        flash("Tu cuenta ha sido cerrada satisfactoriamente", "success_deleted_account")
        return redirect(url_for("index"))

    flash("Debes loguearte primero para acceder a esta seccion.", "error")
    return redirect(url_for("login"))

@app.route("/acc/modificar-datos", methods=["GET", "POST"])
def modificarDatosPersonales():
    if "usermail" in session:

        if request.method == "POST":  # si el usuario hizo click  "Aceptar" y paso las pruebas
            dniRepe = Users.query.filter_by(dni_titular_tarjeta=request.form["titularTarj"]).first()
            if dniRepe:
                if (dniRepe.correo == session["usermail"]):
                    # No modifico su DNI en el form

                    usuario_logueado = session["usermail"]

                    user = Users.query.filter_by(correo=usuario_logueado).first()

                    user.nombre = request.form["nombre"]
                    user.apellido = request.form["apellido"]
                    user.fecha_nac = request.form["nacimiento"]
                    user.clave = request.form["password1"]
                    user.dni_titular_tarjeta = request.form["titularTarj"]
                    user.tipo_tarjeta = request.form["tipos_tarj"]
                    user.num_tarjeta = request.form["numero_de_tarjeta"]
                    user.titular_tarjeta = request.form["nombre_titular_tarjeta"]
                    user.cvc = request.form["cvc_tarj"]
                    user.mes_venc = request.form["exMonth"]
                    user.anio_venc = request.form["exYear"]

                    db.session.commit()

                    flash("La modificación de tus datos personales se ha realizado con éxito", "success_login")
                    return redirect(url_for("index"))
                else:
                    flash("El DNI ingresado esta asociado a otra cuenta de usuario. Intentalo de nuevo.", "error")
            else:
                usuario_logueado = session["usermail"]

                user = Users.query.filter_by(correo=usuario_logueado).first()

                user.nombre = request.form["nombre"]
                user.apellido = request.form["apellido"]
                user.fecha_nac = request.form["nacimiento"]
                user.clave = request.form["password1"]
                user.dni_titular_tarjeta = request.form["titularTarj"]
                user.tipo_tarjeta = request.form["tipos_tarj"]
                user.num_tarjeta = request.form["numero_de_tarjeta"]
                user.titular_tarjeta = request.form["nombre_titular_tarjeta"]
                user.cvc = request.form["cvc_tarj"]
                user.mes_venc = request.form["exMonth"]
                user.anio_venc = request.form["exYear"]

                db.session.commit()

                flash("La modificación de tus datos personales se ha realizado con éxito", "success_login")
                return redirect(url_for("index"))

        c = session["usermail"]
        u = Users.query.filter_by(correo=c).first()
        return render_template("modificar-datos.html", usuario=u)

    flash("Debes loguearte primero para acceder a esta seccion.", "error")
    return redirect(url_for("login"))

@app.route("/perfiles")
def perfiles():
    if "usermail" in session:
        elmail = session["usermail"]
        us = Users.query.filter_by(correo=elmail).first() # Obtiene el usuario a buscar sus perfile

        #2) Filtrar elementos que coincidan: el usuario_id de la tabla perfiles con el id del usuario logueado

        lista = Perfiles.query.filter_by(usuario_id=us.id).all() # se obtienen todos los perfiles del usuario logueado

        perfiles = []

        for perfil in lista:

            if (perfil.perfil_borrado == "False"):

                dic = {"profile_img": " ", "nombre_de_perfil": " "}

                dic["nombre_de_perfil"] = perfil.nombre_perfil
                dic["profile_img"] = perfil.imagen_de_perfil

                perfiles.append(dic)

        # Se creó la lista de diccionarios con los perfiles del usuario

        return render_template("perfiles.html", perfiles=perfiles)

    flash("Debes loguearte primero para acceder a esta sección", "error")
    return redirect(url_for("login"))

@app.route("/perfiles/agregar", methods=['GET', 'POST'])
def agregar_perfil():
    if "usermail" in session:

        # Checkear si ya tiene el numero maximo de perfiles permitido para su membresía
        elmail = session["usermail"]
        us = Users.query.filter_by(correo=elmail).first()
        membresia = us.tipo_de_usuario

        lista = Perfiles.query.filter_by(usuario_id=us.id).all()

        cantidadPerfiles = 0

        for perfill in lista:
            if (perfill.perfil_borrado == "False"):
                cantidadPerfiles = cantidadPerfiles + 1

        if request.method == "POST":

            elmail = session["usermail"]
            us = Users.query.filter_by(correo=elmail).first() # Obtiene al usuario para agregarle el perfil

            new_perfil = Perfiles( usuario_id=us.id,
                                   nombre_perfil=request.form["profile_name"],
                                   imagen_de_perfil=request.form["profile_avatar"],
                                   perfil_borrado="False")

            db.session.add(new_perfil)
            db.session.commit()

            flash("Se ha agregado el nuevo perfil con éxito", "success")
            return redirect(url_for("perfiles"))

        return render_template("agregar-perfil.html", membresia=membresia, cantidadPerfiles=cantidadPerfiles)

    flash("Debes loguearte primero para acceder a esta sección", "error")
    return redirect(url_for("login"))


@app.route("/perfiles/administrar")
def administrar_perfiles():
    if "usermail" in session:
        return render_template("administrar-perfiles.html")

    flash("Debes loguearte primero para acceder a esta seccion.", "error")
    return redirect(url_for("login"))


@app.route("/perfiles/borrar", methods=['GET', 'POST'])
def borrar_perfil():
    if "usermail" in session:
        # Checkear si tiene el numero minimo de perfiles permitidos (1)
        elmail = session["usermail"]
        us = Users.query.filter_by(correo=elmail).first()

        lista = Perfiles.query.filter_by(usuario_id=us.id).all()

        cantidadPerfiles = 0
        perfiles = []

        for perfill in lista:
            if (perfill.perfil_borrado == "False"):
                cantidadPerfiles = cantidadPerfiles + 1;

                dic = {"nombre_perfil_id_perfil": []}

                dic["nombre_perfil_id_perfil"].append(perfill.nombre_perfil)
                dic["nombre_perfil_id_perfil"].append(perfill.id)

                perfiles.append(dic)

        if request.method == "POST":

            # Busca el perfil para marcarlo como borrado
            id_del_perfil_a_borrar = request.form["perfil_borrado"]
            elPerfil = Perfiles.query.filter_by(id=id_del_perfil_a_borrar).first()
            elPerfil.perfil_borrado = "True"

            db.session.commit() # hace efectivo los cambios

            flash("Se ha borrado el perfil con éxito", "success")
            return redirect(url_for("perfiles"))

        return render_template("borrar-perfil.html", cantidadPerfiles=cantidadPerfiles, perfiles=perfiles)

    flash("Debes loguearte primero para acceder a esta sección", "error")
    return redirect(url_for("login"))



# Variable global
id_del_perfil_a_modificar = 0

@app.route("/perfiles/modificar", methods=['GET', 'POST'])
def modificar_perfil():
    if "usermail" in session:

        elmail = session["usermail"]
        us = Users.query.filter_by(correo=elmail).first()

        lista = Perfiles.query.filter_by(usuario_id=us.id).all()

        perfiles = []

        for perfilll in lista:
            if (perfilll.perfil_borrado == "False"):

                dic = {"nombre_perfil_id_perfil": []}

                dic["nombre_perfil_id_perfil"].append(perfilll.nombre_perfil)
                dic["nombre_perfil_id_perfil"].append(perfilll.id)

                perfiles.append(dic)

        if request.method == "POST": #Hizo click en 'Aceptar' y procede a la pagina de modificacion del perfil seleccionado

            global id_del_perfil_a_modificar
            id_del_perfil_a_modificar = request.form["perfil_seleccionado"]
            elPerfil = Perfiles.query.filter_by(id=id_del_perfil_a_modificar).first()

            return render_template("modificando-perfil.html", perfil=elPerfil)

        return render_template("modificar-perfil.html", perfiles=perfiles)

    flash("Debes loguearte primero para acceder a esta sección", "error")
    return redirect(url_for("login"))


@app.route("/perfiles/modificando", methods=['GET', 'POST'])
def modificando_perfil():
    if "usermail" in session:

        if request.method == "POST": # Hizo click en Modificar y pasó las validaciones para la modificacion del perfil

            elPerfil = Perfiles.query.filter_by(id=id_del_perfil_a_modificar).first()

            elPerfil.nombre_perfil = request.form["profile_name"]
            elPerfil.imagen_de_perfil = request.form["profile_avatar"]

            db.session.commit()

            flash("Se ha modificado el perfil con éxito", "success")
            return redirect(url_for("perfiles"))

        flash("Acceso denegado", "error")
        return redirect(url_for("modificar_perfil"))

    flash("Debes loguearte primero para acceder a esta sección", "error")
    return redirect(url_for("login"))


@app.route("/modificarSuscripcion", methods=['POST', 'GET'])
def modificar_suscripcion():
    if "usermail" in session:

        elmail = session["usermail"]
        us = Users.query.filter_by(correo=elmail).first()
        membresia = us.tipo_de_usuario

        lista = Perfiles.query.filter_by(usuario_id=us.id).all()
        cantidadPerfiles = 0

        for perfill in lista:
            if (perfill.perfil_borrado == "False"):
                cantidadPerfiles = cantidadPerfiles + 1

        if request.method == 'POST':
            if (membresia == 1):

                us.tipo_de_usuario = 2
                db.session.commit()

                flash("Ya eres usuario Premium", "success_login")
                return redirect(url_for("index"))
            else:

                us.tipo_de_usuario = 1
                db.session.commit()

                flash("Ya eres usuario Standard", "success_login")
                return redirect(url_for("index"))

        return render_template("modificar-suscripcion.html", membresia=membresia, cantidadPerfiles=cantidadPerfiles)

    flash("Debes loguearte primero para acceder a esta seccion.", "error")
    return redirect(url_for("login"))


@app.route("/novedadesAdm", methods=['POST', 'GET'])
def novedades():
    if request.method == 'POST':
        task_title = request.form['title']
        task_content = request.form['content']
        new_novedad = novedad(title=task_title, content=task_content)

        try:
            db.session.add(new_novedad)
            db.session.commit()
            return redirect('/novedadesAdm')
        except:
            return 'Hubo un problema agregando la novedad'

    else:
        novedades = novedad.query.order_by(novedad.date_created).all()
        return render_template("novedadesAdm.html", novedades=novedades)

@app.route('/borrar/<int:id>')
def borrar(id):
        novedad_a_borrar = novedad.query.get_or_404(id)

        try:
            db.session.delete(novedad_a_borrar)
            db.session.commit()
            return redirect('/novedadesAdm')
        except:
            return 'Hubo un problema borrando la novedad'

@app.route('/actualizarNoticia/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    novedad_a_actualizar = novedad.query.get_or_404(id)

    if request.method == 'POST':
        novedad_a_actualizar.title = request.form['title']
        novedad_a_actualizar.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/novedadesAdm')
        except:
            return 'Hubo un problema actualizando la novedad'
    else:
        return render_template('actualizarNoticia.html', novedad_a_actualizar=novedad_a_actualizar)

@app.route("/novedadesU")
def novedadesU():
    nove = novedad.query.order_by(novedad.date_created).all()
    return render_template("novedadesU.html", nove=nove)

@app.route('/noticia/<int:id>', methods=['GET', 'POST'])
def noticia(id):
        noticia = novedad.query.get_or_404(id)
        return render_template("noticia.html", noticia=noticia)

@app.route("/agregarTrailer")
def agregarTrailer():
    return render_template('formulario.html')


@app.route("/uploader", methods=["GET", "POST"])
def uploader():
    if request.method == "POST":
        if "file" not in request.files:
            return "The form has no file part."
        f = request.files['file']
        if f.filename == "":
            flash ("No hay archivo seleccionado")
            return redirect ("/agregarTrailer")
        trailerR = trailers.query.filter_by(nombre=f.filename).first()
        if trailerR:
            flash ("El archivo ya existe")
            return redirect("/agregarTrailer")
        elif f and allowed_file(f.filename):
            nueT= trailers(nombre= f.filename, file= os.path.join(app.config['UPLOAD_FOLDER']))
            db.session.add(nueT)
            db.session.commit()
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash ("Archivo subido con exito")
            return redirect(url_for("agregarTrailer"))
        flash ("Archivo no soportado.")
        return redirect (url_for("agregarTrailer"))

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/trailersU', methods=['GET', 'POST'])
def trailersU():
    trai = trailers.query.order_by(trailers.id).all()
    lista = []
    listaN = []
    for i in trai:
        if i.libro_id:
            lib = (Libros.query.filter_by(id=i.libro_id).first())
            lista.append([lib, i])
        else:
            listaN.append(i)
    if request.method == "POST":
        filename = request.form['nombre']
        return redirect(url_for('uploaded_file', filename=filename))
    return render_template("trailer_usuario.html", listaN=listaN, lista=lista)

@app.route("/agregarTrailerLibro/<int:id>", methods=["GET", "POST"])
def agregarTrailerLibro(id):
    libro = Libros.query.get_or_404(id)
    if libro.tiene_trailer:
        flash("El libro ya tiene un trailer asignado")
        return redirect ("/traerLibros")
    else:
        if request.method == "POST":
            if "file" not in request.files:
                return "The form has no file part."
            f = request.files['file']
            if f.filename == "":
                flash ("No hay archivo seleccionado")
                return redirect ("/traerLibros")
            trailerR = trailers.query.filter_by(nombre=f.filename).first()
            if trailerR:
                flash ("El archivo ya existe")
                return redirect("/traerLibros")
            elif f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                nueT= trailers(nombre= f.filename, libro_id = libro.id, file= os.path.join(app.config['UPLOAD_FOLDER']))
                db.session.add(nueT)
                libro.archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                libro.tiene_trailer = 1
                db.session.commit()
                flash ("Archivo subido con exito")
                return redirect(url_for("traerLibros"))
            flash ("Archivo no soportado.")
            return redirect (url_for("traerLibros"))
    return render_template ("agregarTrailerLibro.html", libro=libro)

@app.route('/BorrarTrailersAdm')
def trailersAdm():
    trai = trailers.query.order_by(trailers.id).all()
    return render_template('BorrarTrailersAdm.html', trai=trai)

@app.route('/borrarT/<int:id>')
def borrarT(id):
        trailer_a_borrar = trailers.query.get_or_404(id)

        if trailer_a_borrar.libro_id:
            libro = Libros.query.filter_by(id=trailer_a_borrar.libro_id).first()
            if libro.tiene_trailer:
                libro.archivo = ""
                libro.tiene_trailer = 0
        db.session.delete(trailer_a_borrar)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], trailer_a_borrar.nombre))
        db.session.commit()
        flash("Trailer borrado", "success")
        return redirect('/BorrarTrailersAdm')

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        tag = request.form["book"]
        search = "%{}%".format(tag)
        libro = Libros.query.filter(Libros.titulo.ilike(search)).all()
        autor = Autores.query.filter(Autores.nomAutor.ilike(search)).first()
        genero = Generos.query.filter(Generos.nomGenero.ilike(search)).first()
        if (autor != None):
            librosAut = Libros.query.filter_by(autor_id=autor.id).all()
            return render_template("busqueda.html", autor=autor, librosAut=librosAut, genero=genero, libro= libro)
        elif genero != None:
            librosGen = Libros.query.filter_by(genero_id=genero.id).all()
            return render_template("busqueda.html", genero=genero, librosGen=librosGen, autor=autor, libro=libro )
        else:
            return render_template("busqueda.html", libro=libro, genero=genero, autor=autor)
