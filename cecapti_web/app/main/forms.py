from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Optional, NumberRange

# Formulario de inscripción
class InscriptionForm(FlaskForm):
	alumno = QuerySelectField(
		'Alumno',
		query_factory=lambda: Usuarios.query.filter(Usuarios.id_rol==3).all(),  # Ajusta el id_rol si es necesario
		get_label='nombre_completo'
	)
	curso = QuerySelectField(
		'Curso',
		query_factory=lambda: Cursos.query.all(),
		get_label='nombre_curso'
	)
	submit = SubmitField('Inscribir')
from app.models import Roles, Usuarios, Cursos

class GradeForm(FlaskForm):
	grade = FloatField('Calificación', validators=[DataRequired(), NumberRange(min=0, max=20)])
	submit = SubmitField('Guardar')

class UserForm(FlaskForm):
	nombre_usuario = StringField('Nombre de usuario', validators=[DataRequired()])
	password = PasswordField('Contraseña (dejar vacío para no cambiar)', validators=[Optional()])
	nombre_completo = StringField('Nombre completo', validators=[DataRequired()])
	rol = QuerySelectField('Rol', query_factory=lambda: Roles.query.all(), get_label='nombre_rol', allow_blank=False)
	submit = SubmitField('Guardar')

class CourseForm(FlaskForm):
	nombre_curso = StringField('Nombre del curso', validators=[DataRequired()])
	descripcion = TextAreaField('Descripción', validators=[DataRequired()])
	horas_duracion = IntegerField('Horas de duración', validators=[DataRequired()])
	instructor = QuerySelectField('Instructor', query_factory=lambda: Usuarios.query.filter(Usuarios.rol.has(nombre_rol='Instructor')).all(), get_label='nombre_completo', allow_blank=False)
	submit = SubmitField('Guardar')

class MachineryForm(FlaskForm):
	nombre_maquina = StringField('Nombre de la máquina', validators=[DataRequired()])
	identificador = StringField('Identificador', validators=[DataRequired()])
	estado = SelectField('Estado', choices=[('operativa', 'Operativa'), ('en_mantenimiento', 'En mantenimiento'), ('fuera_de_servicio', 'Fuera de servicio')], validators=[DataRequired()])
	submit = SubmitField('Guardar')
