from app import db
from datetime import date, datetime, timedelta


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(70), nullable=False)
    fecha_nac = db.Column(db.String(10), nullable=False)
    correo =  db.Column(db.String(200), unique=True, nullable=False)
    clave =  db.Column(db.String(80), nullable=False)
    dni_titular_tarjeta = db.Column(db.Integer, unique=True, nullable=False)
    tipo_tarjeta = db.Column(db.String(70), nullable=False)
    num_tarjeta = db.Column(db.Integer, nullable=False) # fijarme si hacerla unique
    titular_tarjeta = db.Column(db.String(200), nullable=False)
    cvc = db.Column(db.Integer, nullable=False)
    mes_venc = db.Column(db.String(30), nullable=False)
    anio_venc = db.Column(db.String(4), nullable=False)
    datetime_acceso = db.Column(db.String(200), nullable=True)
    tipo_de_usuario = db.Column(db.Integer, nullable=False)
    deleted_user = db.Column(db.String(5), nullable=False)

class Perfiles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario_id = db.Column(db.Integer, nullable=False)
    nombre_perfil = db.Column(db.String(25), nullable=False)
    imagen_de_perfil = db.Column(db.String(150), nullable=False)
    perfil_borrado = db.Column(db.String(5), nullable=False)

class Libros(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(500))
    ISBN = db.Column(db.Integer)
    editorial_id = db.Column(db.Integer)
    autor_id = db.Column(db.Integer)
    genero_id = db.Column(db.Integer)
    fecha_edicion = db.Column(db.String(10))
    cantCapTotales = db.Column(db.Integer)
    capSubidosAct =  db.Column(db.Integer, default = 0)
    tiene_trailer = db.Column(db.Integer, default=0)
    oculto = db.Column(db.Integer, nullable=False, default = 0)
    pathPortada = db.Column(db.String, default = "../static/imgs/Portadas\default\portadaDefault.jpg")

    
class Capitulos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nomCap = db.Column(db.String(200))
    lib_id = db.Column(db.Integer)
    numCap = db.Column(db.Integer)
    fecha_vencimiento = db.Column(db.DateTime)
    fecha_lanzamiento = db.Column(db.DateTime, default=datetime.now())
    cantidad_de_paginas = db.Column(db.Integer)
    path = db.Column(db.String)


class Editoriales(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nomEditorial = db.Column(db.String(50))

class Autores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nomAutor = db.Column(db.String(50))

class Generos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nomGenero = db.Column(db.String(50))

class novedad(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class trailers(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nombre = db.Column(db.String, nullable=False)
    libro_id = db.Column(db.Integer, nullable=True)
    file = db.Column(db.String)

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    lib_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    perfil_id = db.Column(db.Integer)
    fecha_lectura = db.Column(db.DateTime, default=datetime.utcnow)

class Valoracion(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    lib_id = db.Column(db.Integer, nullable= False)
    user_id = db.Column(db.Integer, nullable= False)
    perfil_id = db.Column(db.Integer, nullable= False)
    puntuacion = db.Column(db.Integer)
    comentario = db.Column(db.String(500))
    fecha_valoracion = db.Column(db.DateTime, default= datetime.utcnow)
    es_spoiler = db.Column(db.Integer, nullable=False, default = 0)
    c_borrado = db.Column(db.Integer, nullable=False, default = 0)      