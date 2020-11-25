import datetime
from db_init import db, FlaskDocument
from passlib.hash import pbkdf2_sha256 as sha256


class User(FlaskDocument):
    email = db.StringField(max_length=255)
    username = db.StringField(max_length=255, unique=True)
    firstname = db.StringField(max_length=255)
    lastname = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    is_admin = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class Cluster(FlaskDocument):
    id = db.StringField(primary_key=True)
    cluster_name = db.StringField(max_length=255, unique=True)
    cluster_id = db.IntField(default=0)


class Usos(FlaskDocument):

    id_trabajador = db.StringField(primary_key=True)
    usos_red = db.IntField(default=0)
    usos_aliados = db.IntField(default=0)
    fecha_alta = db.DateTimeField()
    fecha_modificacion = db.DateTimeField(default=datetime.datetime.now)


class Usuarios(FlaskDocument):

    tipo_id_usurio = db.StringField(required=True, max_length=10)
    id_usuario = db.StringField(primary_key=True)
    nombre_usuario = db.StringField(max_length=200)
    edad = db.IntField(default=0)
    genero = db.StringField(max_length=200)
    estado_vinculacion = db.BooleanField(default=True)
    tipo_afiliacion_usuario = db.StringField(required=True, max_length=100)
    categoria_usuario = db.StringField(required=True, max_length=10)
    tipo_id_trabajador = db.StringField(required=True, max_length=10)
    id_trabajador = db.IntField(default=0)
    tipo_afilacion_trabajador = db.StringField(required=True,  max_length=100)
    fecha_alta = db.DateTimeField()
    fecha_modificacion = db.DateTimeField(default=datetime.datetime.now)

    meta = {'indexes': [
        {'fields': ['$nombre_usuario', "$tipo_afilacion_trabajador", "$tipo_afiliacion_usuario"],
         'default_language': 'Spanish',
         'weights': {'nombre_usuario': 10, 'tipo_afilacion_trabajador': 10, "tipo_afiliacion_usuario": 10}
         }
    ]}
