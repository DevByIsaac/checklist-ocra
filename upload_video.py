from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps

video_routes = Blueprint('routes_cideo', __name__)

@video_routes.route('/cargar_video', methods=['GET', 'POST'])
def cargar_video():
    if 'user_email' not in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Aquí puedes manejar la lógica para procesar el video subido y otros datos del formulario
        # Ejemplo: 
        # video = request.files.get('uploadVideo')
        # if video:
        #     video.save(os.path.join('ruta/a/guardar', video.filename))
        #     # Procesar video o almacenar información adicional
        
        pass  # Eliminar esto cuando agregues la lógica para manejar el POST
        
    # Renderiza la plantilla 'cargar_video.html' cuando se accede con GET o POST (sin lógica adicional)
    return render_template("cargar_video.html")