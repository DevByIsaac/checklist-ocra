from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from functools import wraps
from database import get_all_empleados, get_empleado_by_id
import os
# ##### Imports para los metodos para analisis de videos #####
from modules.analisis_video1 import *
from modules.evaluacion_ocra9 import *

video_routes = Blueprint('video_routes', __name__)
# Variable global para almacenar la ruta del archivo Excel
excel_path = None

@video_routes.route('/cargar_video', methods=['GET'])
def cargar_video():
    if 'user_email' not in session:  # Si no está loggeado el usuario, no muestra esta page
        return redirect(url_for('dashboard'))
    employees = get_all_empleados() # obtenemos empleados para mostrarlos en el <Select>
    #return render_template("cargar_video.html", employees=employees)
    # Obtener el nombre del video procesado de los parámetros de consulta
    #video_filename = request.args.get('video_filename', '')
    #video_url = url_for('static', filename=f'video_marcado/{video_filename}')
    
    return render_template("cargar_video.html", employees=employees)

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
            video_exportado, json_archivo, excel_archivo = process_video(filepath, empleado)
            #draw_keypoints_and_angles(filepath, output_video_folder, json_folder)
            
            flash('Video Procesado exitosamente')
            #return redirect(url_for('video_routes.cargar_video')
            #return redirect(url_for('video_routes.ver_video'))
            #return render_template('cargar_video.html', video_url = video_exportado)
            return render_template('cargar_video.html', video_url=video_exportado, video_filename=os.path.basename(json_archivo), video_filename=os.path.basename(excel_archivo))

            #return redirect(url_for('video_routes.ver_video', video_filename=video_exportado))

    
    return render_template("cargar_video.html")

@video_routes.route('/ver_video', methods=['GET'])
def ver_video():
    video_filename = request.args.get('video_filename', '')
    #video_url = os.path.join('static/video_marcado/', video_filename)
    print(video_url)
    print(video_filename)
    video_url = url_for('static', filename=f'video_marcado/{video_filename}')
    return render_template('cargar_video.html', video_url=video_url)

# Ruta para generar el archivo Excel
@video_routes.route('/generate_excel', methods=['POST'])
def generate_excel():
    global excel_path
    # Aquí defines y generas tu archivo Excel
    # Por ejemplo:
    excel_path = '/path/to/your/excel_file.xlsx'
    # Guardar el archivo Excel
    wb.save(excel_path)
    return jsonify({"message": "Archivo Excel generado"})

@video_routes.route('/descargar_excel', methods=['GET'])
def descargar_excel():
    video_filename = request.args.get('video_filename', '')
    excel_path = os.path.join('static/resultados/', video_filename)
    #excel_url = url_for('static', filename=f'resultados/{video_filename}')
    #return render_template('cargar_video.html', excel_url=excel_url)
    if not os.path.isfile(excel_path):
        flash('Archivo Excel no encontrado')
        return redirect(url_for('video_routes.cargar_video'))
    
    return send_file(excel_path, as_attachment=True)

@video_routes.route('/descargar_json', methods=['GET'])
def descargar_json():
    video_filename = request.args.get('video_filename', '')
    json_path = os.path.join('static/json/', video_filename)
    #json_url = url_for('static', filename=f'json/{video_filename}')
    if not os.path.isfile(json_path):
        flash('Archivo JSON no encontrado')
        return redirect(url_for('video_routes.cargar_video'))
    
    return send_file(json_path, as_attachment=True)
    #return render_template('cargar_video.html', json_url=json_url)

def allowed_file(filename):
    # Solo permite .mp4 (eso creo)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  {'mp4'}

