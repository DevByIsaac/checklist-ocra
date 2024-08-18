from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TimeField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from database import create_empleado, update_empleado, delete_empleado, get_all_empleados, get_empleado_by_id

employee_routes = Blueprint('routes_emp', __name__)


class RegistroEmpleadoForm(FlaskForm):
    rol = StringField('Rol', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')], validators=[DataRequired()])
    edad = IntegerField('Edad', validators=[DataRequired()])
    puesto = StringField('Puesto', validators=[DataRequired()])
    estatura = DecimalField('Estatura', validators=[DataRequired()])
    duracion_turno = TimeField('Duración del Turno', format='%H:%M', validators=[DataRequired()])
    duracion_descanso = TimeField('Duración del Descanso', format='%H:%M', validators=[DataRequired()])
    duracion_tiempo_libre = TimeField('Duración del Tiempo Libre', format='%H:%M', validators=[DataRequired()])
    # created_by = StringField('Creado Por', validators=[DataRequired()])
    # updated_by = StringField('Actualizado Por', validators=[DataRequired()])
    submit = SubmitField('Registrar Empleado')



@employee_routes.route('/registro_empleado', methods=['GET', 'POST'])
def registro_empleado():
    form = RegistroEmpleadoForm()
    if form.validate_on_submit():
        create_empleado(
            form.rol.data,
            form.nombre.data,
            form.apellido.data,
            form.sexo.data,
            form.edad.data,
            form.puesto.data,
            form.estatura.data,
            form.duracion_turno.data,
            form.duracion_descanso.data,
            session['user_email'],
            session['user_email'],
        )
        flash('Creado Empleado con éxito!', 'success')

    return render_template('registro_empleado.html', form=form)