from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from database import get_all_empleados, get_empleado_by_id
import os
# ##### Imports para los metodos para analisis de videos #####
from modules.analisis_video1 import *

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/cargar_video', methods=['GET'])
def cargar_video():
    if 'user_email' not in session:  # Si no está loggeado el usuario, no muestra esta page
        return redirect(url_for('dashboard'))
    employees = get_all_empleados() # obtenemos empleados para mostrarlos en el <Select>
    #return render_template("cargar_video.html", employees=employees)
    # Obtener el nombre del video procesado de los parámetros de consulta
    video_filename = request.args.get('video_filename', '')
    video_url = url_for('static', filename=f'video_marcado/{video_filename}')
    
    return render_template("cargar_video.html", employees=employees, video_url=video_url)

@video_routes.route('/upload_video', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No hay archivos en la petición')
            return redirect(request.url)
        
        file = request.files['file']
        empleado_id = int(request.form.get("empleado"))
        empleado = get_empleado_by_id(empleado_id)

        if file.filename == '':
            flash('Archivo sin nombre')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Guardamos el video en la carpeta uploads
            filepath = os.path.join('static/uploads/', file.filename)
            file.save(filepath)
       
            # Aqui llamamos todas las funciones que nos de la gana...
            process_video(filepath, empleado)
            #draw_keypoints_and_angles(filepath, output_video_folder, json_folder)
            
            flash('Video Procesado exitosamente')
            #return redirect(url_for('video_routes.cargar_video')
            return redirect(url_for('video_routes.cargar_video'))

    
    return render_template("cargar_video.html")

@video_routes.route('/ver-video')
def video_view():
    video_filename = request.args.get('video_filename', '')
    video_url = url_for('static', filename=f'video_marcado/{video_filename}')
    return render_template('cargar_video.html', video_url=video_url)


def allowed_file(filename):
    # Solo permite .mp4 (eso creo)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  {'mp4'}

