import psycopg2
from psycopg2 import errors
from flask import current_app, g, flash
from config import Config

def get_db_connection():
    g.db_connection = psycopg2.connect(
        dbname=current_app.config['DB_NAME'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        host=current_app.config['DB_HOST'],
        port=current_app.config['DB_PORT']
    )
    return g.db_connection

def close_db_connection(e=None):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()

def authenticate_user(email, password):
    db_connection = get_db_connection()
    try:
        with db_connection.cursor() as cursor:
            cursor.callproc('public.authenticate_user', [email, password])
            result = cursor.fetchone()
            return result[0] == 'success' if result else False
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return False

def create_user_procedure(username, email, password, created_by, updated_by):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Usa execute con la instrucción CALL directamente
        cursor.execute('CALL public.create_user(%s, %s, %s, %s, %s)', 
                       (username, email, password, created_by, updated_by))
        conn.commit()
        return True
    except errors.UniqueViolation as e:
        # Capturar y manejar la excepción si el usuario ya existe
        flash('El correo ya está registrado', 'error')
        print(f'Error creando el usuario: {e}')
        conn.rollback()
        return False
    except Exception as e:
        # Manejar otras excepciones
        flash('Error inesperado al crear el usuario. Inténtalo de nuevo.', 'error')
        print(f'Error creando el usuario: {e}')
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id):
    db_connection = get_db_connection()
    with db_connection.cursor() as cursor:
        cursor.callproc('public.get_user_by_id', [user_id])
        result = cursor.fetchone()
        return result if result else None

def create_empleado(rol, nombre, apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT public.insert_employee(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (rol, nombre, apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by))
            result = cursor.fetchone()[0]
            conn.commit()
    finally:
        conn.close()
    return result


def create_actividad(usuario_id, tipo_actividad, descripcion, actividad_repetitiva, num_pausas, lunch_break_duration, puntaje_ATD, puntaje_ATE, puntaje_acciones_fuerza, puntaje_FSO, puntaje_FFM, created_by, updated_by):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL public.create_actividad(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (usuario_id, tipo_actividad, descripcion, actividad_repetitiva, num_pausas,
                  lunch_break_duration, puntaje_ATD, puntaje_ATE, puntaje_acciones_fuerza,
                  puntaje_FSO, puntaje_FFM, created_by, updated_by))
            conn.commit()
    finally:
        conn.close()

def get_all_empleados():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT empleado_id, nombre, apellido FROM empleado')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            empleados = [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()
    return empleados

def get_empleado_by_id(empleado_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by FROM Empleado WHERE empleado_id = %s", (str(empleado_id),))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                empleado = dict(zip(columns, row))
            else:
                empleado = None
    finally:
        conn.close()
    return empleado

def get_actividad_by_empleado_id(empleado_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_actividad, empleado_id, tipo_actividad, descripcion, actividad_repetitiva, num_pausas, lunch_break_duration, puntaje_atd, puntaje_ate, puntaje_acciones_fuerza, puntaje_fso, puntaje_ffm, created_by, updated_by FROM public.actividades WHERE empleado_id = %s LIMIT 1", (str(empleado_id),))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                empleado = dict(zip(columns, row))
            else:
                empleado = None
    finally:
        conn.close()
    return empleado