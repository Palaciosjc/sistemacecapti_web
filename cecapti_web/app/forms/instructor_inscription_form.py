from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms import SubmitField
from app.models import Usuarios

class InstructorInscriptionForm(FlaskForm):
    alumno = QuerySelectField(
        'Alumno',
        query_factory=lambda: Usuarios.query.filter(Usuarios.id_rol==3).all(),
        get_label='nombre_completo',
        validators=[DataRequired()]
    )
    submit = SubmitField('Inscribir')
