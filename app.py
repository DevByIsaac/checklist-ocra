from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import authenticate_user, create_user_procedure
from database import create_empleado, create_actividad, get_empleado_by_id
from info import info_routes
from employee import employee_routes
from upload_video import video_routes

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(info_routes)
app.register_blueprint(employee_routes)
app.register_blueprint(video_routes)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate_user(email, password):
            session['user_email'] = email
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error en el inicio de sesión. Verifica tu correo electrónico y/o contraseña.', 'danger')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        created_by = email
        updated_by = email
        
        if create_user_procedure(username, email, password, created_by, updated_by):
            flash('¡Registro exitoso! Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error en el registro. Por favor, intenta nuevamente.', 'danger')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))
    
    user_email = session['user_email']
    return render_template('dashboard.html', user_email=user_email)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has sido desconectado.', 'info')
    return redirect(url_for('login'))

@app.route('/create_empleado', methods=['POST'])
def create_empleado_route():
    data = request.json
    try:
        create_empleado(
            data['rol'],
            data['nombre'],
            data['apellido'],
            data['sexo'],
            data['edad'],
            data['puesto'],
            data.get('duracion_turno', None),  # Usar valor por defecto si no está presente
            data.get('duracion_descanso', None),
            data.get('duracion_tiempo_libre', None),
            data['created_by'],
            data['updated_by']
        )
        return jsonify({'message': 'Empleado creado con éxito'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/empleado/<int:empleado_id>', methods=['GET'])
def get_empleado(empleado_id):
    try:
        empleado = get_empleado_by_id(empleado_id)
        if empleado:
            return jsonify(empleado), 200
        else:
            return jsonify({'message': 'Empleado no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_actividad', methods=['POST'])
def create_actividad_route():
    data = request.json
    try:
        create_actividad(
            data['usuario_id'],
            data['tipo_actividad'],
            data['descripcion'],
            data['actividad_repetitiva'],
            data['num_pausas'],
            data['lunch_break_duration'],
            data['puntaje_ATD'],
            data['puntaje_ATE'],
            data['puntaje_acciones_fuerza'],
            data['puntaje_FSO'],
            data['puntaje_FFM'],
            data['created_by'],
            data['updated_by']
        )
        return jsonify({'message': 'Actividad creada con éxito'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)