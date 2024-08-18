import psycopg2
from flask import current_app, g
from config import Config

def get_db_connection():
    if 'db_connection' not in g:
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
    except Exception as e:
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

def create_empleado(rol, nombre, apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, created_by, updated_by):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL public.create_empleado(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (rol, nombre, apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, created_by, updated_by))
            conn.commit()
    finally:
        conn.close()

def update_empleado(empleado_id, rol, nombre, apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, updated_by):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL public.update_empleado(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (empleado_id, rol, nombre, apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, updated_by))
            conn.commit()
    finally:
        conn.close()

def delete_empleado(empleado_id, updated_by):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL public.delete_empleado(
                    %s, %s
                )
            """, (empleado_id, updated_by))
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
            cursor.execute("CALL public.get_empleado_by_id(%s)", (empleado_id,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                empleado = dict(zip(columns, row))
            else:
                empleado = None
    finally:
        conn.close()
    return empleado