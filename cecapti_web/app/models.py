from . import db
from flask_login import UserMixin
import bcrypt

class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50))
    usuarios = db.relationship('Usuarios', backref='rol', lazy=True)

class Usuarios(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True)
    clave_hash = db.Column(db.String(255))
    nombre_completo = db.Column(db.String(150))
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    session_token = db.Column(db.Text)
    cursos = db.relationship('Cursos', backref='instructor', lazy=True, foreign_keys='Cursos.id_instructor')

    def get_id(self):
        return str(self.id_usuario)

    def set_password(self, password):
        self.clave_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.clave_hash.encode('utf-8'))

class Cursos(db.Model):
    __tablename__ = 'cursos'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    horas_duracion = db.Column(db.Integer)
    id_instructor = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))



# Modelo de Maquinaria
class Maquinaria(db.Model):
    __tablename__ = 'maquinaria'
    id_maquinaria = db.Column(db.Integer, primary_key=True)
    nombre_maquina = db.Column(db.String(100))
    identificador = db.Column(db.String(50))
    estado = db.Column(db.String(30))  # operativa, en_mantenimiento, fuera_de_servicio

# Modelo de Inscripciones
class Inscripciones(db.Model):
    __tablename__ = 'inscripciones'
    id_inscripcion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_alumno = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'))
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso', ondelete='CASCADE'))
    fecha_inscripcion = db.Column(db.Date, nullable=False)
    calificacion_final = db.Column(db.Float, nullable=True)

    alumno = db.relationship('Usuarios', backref=db.backref('inscripciones', cascade='all, delete-orphan'), foreign_keys=[id_alumno])
    curso = db.relationship('Cursos', backref=db.backref('inscripciones', cascade='all, delete-orphan'), foreign_keys=[id_curso])
