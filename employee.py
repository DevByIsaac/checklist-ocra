from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TimeField, SubmitField
from wtforms.validators import DataRequired
from database import create_empleado, create_actividad, get_user_by_id, get_all_empleados

employee_routes = Blueprint('routes_emp', __name__)

class RegistroEmpleadoForm(FlaskForm):
    rol = StringField('Rol', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')], validators=[DataRequired()])
    edad = IntegerField('Edad', validators=[DataRequired()])
    puesto = StringField('Puesto', validators=[DataRequired()])
    duracion_turno = IntegerField('Duración del Turno (minutos)', validators=[DataRequired()])
    duracion_descanso = IntegerField('Duración del Descanso (minutos)', validators=[DataRequired()])
    duracion_tiempo_libre = IntegerField('Duración del Tiempo Libre (minutos)', validators=[DataRequired()])
    #created_by = StringField('Creado Por', validators=[DataRequired()])
    #updated_by = StringField('Actualizado Por', validators=[DataRequired()])
    
    #Actividades
    #usuario_id = get_user_by_id
    tipo_actividad = StringField('Tipo de Actividad', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    actividad_repetitiva = SelectField('Actividad Repetitiva', choices=[('true', 'Sí'), ('false', 'No')], validators=[DataRequired()])
    num_pausas = SelectField('Número de Pausas', choices=[
        ('0', 'No existen pausas reales, excepto de unos pocos minutos (menos de 5) en 7-8 horas de turno.'),
        ('1', 'Existe 1 pausa, de al menos 8 minutos, en un turno de 6 horas.'),
        ('1', 'Existe 1 pausa, de al menos 8 minutos, en un turno de 7 horas sin descanso para almorzar.'),
        ('2', 'Existen 2 pausas, de al menos 8 minutos, en un turno de 6 horas (sin descanso para el almuerzo).'),
        ('2', 'Existen 2 pausas, de al menos 8 minutos, además del descanso para el almuerzo, en un turno de 7-8 horas.'),
        ('3', 'Existen 3 pausas, de al menos 8 minutos, además del descanso para el almuerzo, en un turno de 7-8 horas.'),
        ('3', 'Existen 3 pausas (sin descanso para el almuerzo), de al menos 8 minutos, en un turno de 7-8 horas.'),
        ('4', 'Existen al menos 4 interrupciones (además del descanso para el almuerzo) de al menos 8 minutos en un turno de 7-8 horas.'),
        ('4', 'Existen 4 interrupciones de al menos 8 minutos en un turno de 6 horas (sin descanso para el almuerzo).'),
        ('1', 'El periodo de recuperación está incluido en el ciclo de trabajo (al menos 10 segundos consecutivos de cada 60, en todos los ciclos de todo el turno).'),
        ('1', 'Existe una interrupción de al menos 8 minutos cada hora de trabajo (contando el descanso del almuerzo).')
    ], validators=[DataRequired()])
    lunch_break_duration = IntegerField('Duración del Almuerzo (minutos)')
    acciones_tecnicas_dinamicas = SelectField('Acciones Técnicas Dinámicas', choices=[
        ('0', 'No requiere acción'),
        ('0', 'Movimientos del brazo son lentos (20 acciones/minuto). Se permiten pequeñas pausas frecuentes.'),
        ('1', 'Movimientos del brazo no son demasiado rápidos (30 acciones/minuto). Se permiten pequeñas pausas.'),
        ('3', 'Movimientos del brazo son bastante rápidos (más de 40 acciones/minuto). Se permiten pequeñas pausas.'),
        ('4', 'Movimientos del brazo son bastante rápidos (más de 40 acciones/minuto). Sólo se permiten pequeñas pausas ocasionales e irregulares.'),
        ('6', 'Movimientos del brazo son rápidos (más de 50 acciones/minuto). Sólo se permiten pequeñas pausas ocasionales e irregulares.'),
        ('8', 'Movimientos del brazo son rápidos (más de 60 acciones/minuto). La carencia de pausas dificulta el mantenimiento del ritmo.'),
        ('10', 'Movimientos del brazo se realizan con una frecuencia muy alta (70 acciones/minuto o más). No se permiten las pausas.')
    ], validators=[DataRequired()])
    acciones_tecnicas_estaticas = SelectField('Acciones Técnicas Estáticas', choices=[
        ('0', 'No requiere acción'),
        ('2.5', 'Se sostiene un objeto durante al menos 5 segundos consecutivos realizándose una o más acciones estáticas durante 2/3 del tiempo de ciclo (o de observación).'),
        ('4.5', 'Se sostiene un objeto durante al menos 5 segundos consecutivos realizándose una o más acciones estáticas durante 3/3 del tiempo de ciclo (o de observación).')
    ], validators=[DataRequired()])
    puntaje_acciones_fuerza = SelectField('Puntaje Acciones de Fuerza', choices=[
        ('2', 'Fuerza Moderada (Esfuerzo CR-10: 3 o 4) - 1/3 del tiempo'),
        ('4', 'Fuerza Moderada (Esfuerzo CR-10: 3 o 4) - 50% del Tiempo'),
        ('6', 'Fuerza Moderada (Esfuerzo CR-10: 3 o 4) - >50% del tiempo'),
        ('8', 'Fuerza Moderada (Esfuerzo CR-10: 3 o 4) - Casi todo el tiempo'),
        ('4', 'Fuerza Intensa (Esfuerzo CR-10: 5 o 6) - 2 seg. cada 10 min.'),
        ('8', 'Fuerza Intensa (Esfuerzo CR-10: 5 o 6) - 1% del tiempo'),
        ('16', 'Fuerza Intensa (Esfuerzo CR-10: 5 o 6) - 5% del tiempo'),
        ('24', 'Fuerza Intensa (Esfuerzo CR-10: 5 o 6) - > 10% del tiempo'),
        ('6', 'Fuerza Casi Máxima (Esfuerzo CR-10: 7 o más) - 2 seg. cada 10 min.'),
        ('12', 'Fuerza Casi Máxima (Esfuerzo CR-10: 7 o más) - 1% del tiempo'),
        ('24', 'Fuerza Casi Máxima (Esfuerzo CR-10: 7 o más) - 5% del tiempo'),
        ('32', 'Fuerza Casi Máxima (Esfuerzo CR-10: 7 o más) - > 10% del tiempo')
    ], validators=[DataRequired()])
    factores_socio_organizativos = SelectField('Factores Socio-Organizativos (Fso)', choices=[
        ('1', 'El ritmo de trabajo está parcialmente determinado por la máquina, con pequeños lapsos de tiempo en los que el ritmo de trabajo puede disminuirse o acelerarse'),
        ('2', 'El ritmo de trabajo está totalmente determinado por la máquina')
    ], validators=[DataRequired()])
    factores_fisico_mecanicos = SelectField('Factores Físico-Mecánicos (Ffm)', choices=[
        ('2', 'Se utilizan guantes inadecuados (que interfieren en la destreza de sujeción requerida por la tarea) más de la mitad del tiempo'),
        ('2', 'La actividad implica golpear (con un martillo, golpear con un pico sobre superficies duras, etc.) con una frecuencia de 2 veces por minuto o más'),
        ('2', 'La actividad implica golpear (con un martillo, golpear con un pico sobre superficies duras, etc.) con una frecuencia de 10 veces por hora o más'),
        ('2', 'Existe exposición al frío (menos de 0º) más de la mitad del tiempo'),
        ('2', 'Se utilizan herramientas que producen vibraciones de nivel bajo/medio 1/3 del tiempo o más'),
        ('2', 'Se utilizan herramientas que producen vibraciones de nivel alto 1/3 del tiempo o más'),
        ('2', 'Las herramientas utilizadas causan compresiones en la piel (enrojecimiento, callosidades, ampollas, etc.)'),
        ('2', 'Se realizan tareas de precisión más de la mitad del tiempo (tareas sobre áreas de menos de 2 o 3 mm.)'),
        ('2', 'Existen varios factores adicionales concurrentes, y en total ocupan más de la mitad del tiempo'),
        ('3', 'Existen varios factores adicionales concurrentes, y en total ocupan todo el tiempo')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar Empleado')
    #submit = SubmitField('Registrar Actividad')
    

@employee_routes.route('/registro_empleado', methods=['GET', 'POST'])
def registro_empleado():
    form = RegistroEmpleadoForm()
    if request.method == 'GET':
        # Obtener empleados de la base de datos
        employees = get_all_empleados()
        return render_template('registro_empleado.html', form=form)   
    if form.validate_on_submit():
        empleado_id = create_empleado(
            form.rol.data,
            form.nombre.data,
            form.apellido.data,
            form.sexo.data,
            int(form.edad.data),
            form.puesto.data,
            int(form.duracion_turno.data),
            int(form.duracion_descanso.data),
            int(form.duracion_tiempo_libre.data),
            "admin",
            "admin"
        )
        print(empleado_id)
        create_actividad(
            empleado_id,
            form.tipo_actividad.data,
            form.descripcion.data,
            form.actividad_repetitiva.data == 'true',
            form.num_pausas.data,
            form.lunch_break_duration.data,
            form.acciones_tecnicas_dinamicas.data,
            form.acciones_tecnicas_estaticas.data,
            form.puntaje_acciones_fuerza.data,
            form.factores_socio_organizativos.data,
            form.factores_fisico_mecanicos.data,
            "admin",
            "admin"
        )
        flash('Empleado Creado con éxito!', 'success')
    else:
        print("Formulario no válido")
        print("Errores del formulario:", form.errors)
    # Obtener empleados de la base de datos
    employees = get_all_empleados()
    return render_template('registro_empleado.html', form=form)