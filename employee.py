from flask import Blueprint, render_template, request, redirect, url_for, flash
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TimeField, SubmitField
from wtforms.validators import DataRequired

employee_routes = Blueprint('routes_emp', __name__)


class RegistroEmpleadoForm(FlaskForm):
    rol = StringField('Rol', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')], validators=[DataRequired()])
    edad = IntegerField('Edad', validators=[DataRequired()])
    puesto = StringField('Puesto', validators=[DataRequired()])
    duracion_turno = TimeField('Duración del Turno', format='%H:%M', validators=[DataRequired()])
    duracion_descanso = TimeField('Duración del Descanso', format='%H:%M', validators=[DataRequired()])
    duracion_tiempo_libre = TimeField('Duración del Tiempo Libre', format='%H:%M', validators=[DataRequired()])
    created_by = StringField('Creado Por', validators=[DataRequired()])
    updated_by = StringField('Actualizado Por', validators=[DataRequired()])
    submit = SubmitField('Registrar')



@employee_routes.route('/registro_empleado', methods=['GET', 'POST'])
def registro_empleado():
    form = RegistroEmpleadoForm()
    if form.validate_on_submit():
        # Aquí iría el código para procesar el formulario
        # Ejemplo de redirección después de procesar el formulario
        return redirect(url_for('registro_empleado'))
    
    return render_template('registro_empleado.html', form=form)