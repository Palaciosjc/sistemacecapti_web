
from . import main
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Usuarios, Cursos, Maquinaria, Roles, Inscripciones
from app import db
from .forms import UserForm, CourseForm, MachineryForm, InscriptionForm
import csv
import io
from flask import send_file
# --- ADMIN: Gestión de Inscripciones ---
@main.route('/admin/inscriptions')
@login_required
def admin_inscriptions():
    if getattr(current_user.rol, 'nombre_rol', '').lower() != 'administrador':
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    inscripciones = Inscripciones.query.all()
    return render_template('admin/inscriptions.html', inscripciones=inscripciones)

@main.route('/admin/inscriptions/export')
@login_required
def export_inscriptions():
    inscripciones = Inscripciones.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Alumno', 'Curso'])
    for i in inscripciones:
        cw.writerow([i.id_inscripcion, i.alumno.nombre_completo, i.curso.nombre_curso])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='inscripciones.csv')

@main.route('/admin/inscription/add', methods=['GET', 'POST'])
@login_required
def add_inscription():
    if getattr(current_user.rol, 'nombre_rol', '').lower() != 'administrador':
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    form = InscriptionForm()
    if form.validate_on_submit():
        insc = Inscripciones(
            id_alumno=form.alumno.data.id_usuario,
            id_curso=form.curso.data.id_curso,
            fecha_inscripcion=db.func.current_date()
        )
        db.session.add(insc)
        db.session.commit()
        flash('Inscripción creada correctamente', 'success')
        return redirect(url_for('main.admin_inscriptions'))
    return render_template('admin/inscription_form.html', form=form)

@main.route('/admin/inscription/delete/<int:id>', methods=['POST'])
@login_required
def delete_inscription(id):
    if getattr(current_user.rol, 'nombre_rol', '').lower() != 'administrador':
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    insc = Inscripciones.query.get_or_404(id)
    db.session.delete(insc)
    db.session.commit()
    flash('Inscripción eliminada', 'success')
    return redirect(url_for('main.admin_inscriptions'))

# --- ADMIN: Gestión de Usuarios ---
@main.route('/admin/users')
@login_required
def admin_users():
    if getattr(current_user.rol, 'nombre_rol', '').lower() != 'administrador':
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    usuarios = Usuarios.query.all()
    return render_template('admin/users.html', usuarios=usuarios)

# --- ADMIN: Gestión de Cursos ---
@main.route('/admin/courses')
@login_required
def admin_courses():
    if getattr(current_user.rol, 'nombre_rol', '').lower() != 'administrador':
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    cursos = Cursos.query.all()
    return render_template('admin/courses.html', cursos=cursos)

# --- ADMIN: Gestión de Maquinaria ---
@main.route('/admin/machinery')
@login_required
def admin_machinery():
    if getattr(current_user.rol, 'nombre_rol', '').lower() != 'administrador':
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    maquinaria = Maquinaria.query.all()
    return render_template('admin/machinery.html', maquinaria=maquinaria)

# Página de bienvenida post-login
@main.route('/')
@login_required
def index():
    rol = getattr(current_user.rol, 'nombre_rol', '').lower()
    if rol == 'administrador':
        user_count = Usuarios.query.count()
        course_count = Cursos.query.count()
        machinery_count = Maquinaria.query.count()
        inscription_count = Inscripciones.query.count()
        machinery_status_labels = ['Operativa', 'En Mantenimiento', 'Fuera de Servicio']
        machinery_status_data = [
            Maquinaria.query.filter_by(estado='operativa').count(),
            Maquinaria.query.filter_by(estado='en_mantenimiento').count(),
            Maquinaria.query.filter_by(estado='fuera_de_servicio').count()
        ]
        return render_template(
            'index.html',
            user_count=user_count,
            course_count=course_count,
            machinery_count=machinery_count,
            inscription_count=inscription_count,
            machinery_status_labels=machinery_status_labels,
            machinery_status_data=machinery_status_data
        )
    else:
        return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    rol = getattr(current_user.rol, 'nombre_rol', '').lower()
    if rol == 'administrador':
        usuarios = Usuarios.query.all()
        cursos = Cursos.query.all()
        maquinaria = Maquinaria.query.all()
        return render_template('admin_dashboard.html', usuarios=usuarios, cursos=cursos, maquinaria=maquinaria)
    elif rol == 'instructor':
        cursos = Cursos.query.filter_by(id_instructor=current_user.id_usuario).all()
        # Calcular alumnos totales y pendientes por calificar
        alumnos_totales = sum(len(c.inscripciones) for c in cursos)
        pendientes = sum(
            sum(1 for ins in c.inscripciones if ins.calificacion_final is None)
            for c in cursos
        )
        return render_template(
            'instructor_dashboard.html',
            cursos=cursos,
            alumnos_totales=alumnos_totales,
            pendientes=pendientes
        )
    elif rol == 'alumno':
        inscripciones = Inscripciones.query.filter_by(id_alumno=current_user.id_usuario).all()
        return render_template('student_dashboard.html', inscripciones=inscripciones)
    else:
        return redirect(url_for('main.index'))

# CRUD USUARIOS
@main.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Usuarios(
            nombre_usuario=form.nombre_usuario.data,
            nombre_completo=form.nombre_completo.data,
            rol=form.rol.data
        )
        if form.password.data:
            user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('form.html', form=form, title='Agregar Usuario')

@main.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = Usuarios.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if request.method == 'POST' and form.validate_on_submit():
        user.nombre_usuario = form.nombre_usuario.data
        user.nombre_completo = form.nombre_completo.data
        user.rol = form.rol.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Usuario actualizado', 'success')
        return redirect(url_for('main.dashboard'))
    form.password.data = ''
    return render_template('form.html', form=form, title='Editar Usuario')

@main.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = Usuarios.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado', 'success')
    return redirect(url_for('main.dashboard'))

# CRUD CURSOS
@main.route('/admin/course/add', methods=['GET', 'POST'])
@login_required
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Cursos(
            nombre_curso=form.nombre_curso.data,
            descripcion=form.descripcion.data,
            horas_duracion=form.horas_duracion.data,
            instructor=form.instructor.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Curso creado exitosamente', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('form.html', form=form, title='Agregar Curso')

@main.route('/admin/course/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Cursos.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if request.method == 'POST' and form.validate_on_submit():
        course.nombre_curso = form.nombre_curso.data
        course.descripcion = form.descripcion.data
        course.horas_duracion = form.horas_duracion.data
        course.instructor = form.instructor.data
        db.session.commit()
        flash('Curso actualizado', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('form.html', form=form, title='Editar Curso')



@main.route('/admin/machinery/delete/<int:machinery_id>', methods=['POST'])
@login_required
def delete_machinery(machinery_id):
    m = Maquinaria.query.get_or_404(machinery_id)
    db.session.delete(m)
    db.session.commit()
    flash('Maquinaria eliminada', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/admin/course/delete/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Cursos.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Curso eliminado', 'info')
    return redirect(url_for('main.dashboard'))

# --- CRUD MAQUINARIA ---
@main.route('/admin/machinery/add', methods=['GET', 'POST'])
@login_required
def add_machinery():
    form = MachineryForm()
    if form.validate_on_submit():
        m = Maquinaria(
            nombre_maquina=form.nombre_maquina.data,
            identificador=form.identificador.data,
            estado=form.estado.data
        )
        db.session.add(m)
        db.session.commit()
        flash('Maquinaria agregada', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('form_machinery.html', form=form, action='Agregar')

@main.route('/admin/machinery/edit/<int:machinery_id>', methods=['GET', 'POST'])
@login_required
def edit_machinery(machinery_id):
    m = Maquinaria.query.get_or_404(machinery_id)
    form = MachineryForm(obj=m)
    if request.method == 'POST' and form.validate_on_submit():
        m.nombre_maquina = form.nombre_maquina.data
        m.identificador = form.identificador.data
        m.estado = form.estado.data
        db.session.commit()
        flash('Maquinaria actualizada', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('form_machinery.html', form=form, action='Editar')

