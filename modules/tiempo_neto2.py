import os
import glob
import json
import cv2
from modules.analisis_video1 import *
from config import JSON_FOLDER, VIDEO_MARCADO_FOLDER

def get_most_recent_file(json_folder, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    list_of_files = glob.glob(os.path.join(json_folder, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {json_folder}.")
    return max(list_of_files, key=os.path.getmtime)

def get_duration_from_video(video_path):
    """Calcula la duración total del video en minutos."""
    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise ValueError(f"No se pudo abrir el video en {video_path}.")
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / fps
        video.release()
        return duration_sec / 60  # Convertir a minutos
    except Exception as e:
        raise RuntimeError(f"Error al calcular la duración del video: {e}")

def get_non_repetitive_work_time(video_data):
    """Obtiene el tiempo de trabajo no repetitivo en minutos."""
    try:
        non_repetitive_time = sum(activity['duration'] for activity in video_data['activities'] if not activity['is_repetitive'])
        return non_repetitive_time / 60  # Convertir a minutos
    except KeyError as e:
        raise KeyError(f"Falta una clave en los datos del video: {e}")

def get_breaks_and_rest_time(video_data):
    """Identifica el tiempo de pausas y descansos en minutos."""
    try:
        pauses = sum(break_time['duration'] for break_time in video_data.get('breaks', []))
        rest = sum(rest_time['duration'] for rest_time in video_data.get('rests', []))
        return pauses / 60, rest / 60  # Convertir a minutos
    except KeyError as e:
        raise KeyError(f"Falta una clave en los datos del video: {e}")

def get_number_of_cycles(video_data):
    """Cuenta el número de ciclos de trabajo."""
    try:
        return video_data.get('cycles_count', 0)
    except KeyError as e:
        raise KeyError(f"Falta una clave en los datos del video: {e}")
    
def tiempo_neto(empleado, actividad):
    # Encuentra el archivo JSON y el video más recientes
    json_path = get_most_recent_file(JSON_FOLDER, '.json')
    video_path = get_most_recent_file(VIDEO_MARCADO_FOLDER, '.mp4')
    #actividad = get_actividad_by_empleado_id(empleado["empleado_id"])
    if json_path is None or video_path is None:
        raise FileNotFoundError("No se encontraron archivos JSON o de video en las carpetas especificadas.")

    print(f"Archivo JSON más reciente: {json_path}")
    print(f"Video más reciente: {video_path}")

    # Extraer datos del video
    duration_total = get_duration_from_video(video_path)
    video_data = {
        'activities': [{'duration': empleado["duracion_turno"], 'is_repetitive': actividad["actividad_repetitiva"]}],
        'rests': [{'duration': empleado["duracion_descanso"]}], # Ejemplo de datos
        'cycles_count': 9000  # este campo quedará fijo con 9000 ciclos
    }

    # Calcular TNTR y TNC
    try:
        DT = duration_total
        TNR = get_non_repetitive_work_time(video_data)
        P, A = get_breaks_and_rest_time(video_data)
        NC = get_number_of_cycles(video_data)

        if NC == 0:
            raise ValueError("El número de ciclos no puede ser cero.")

        TNTR = DT - (TNR + P + A)
        TNC = 60 * TNTR / NC

        # Leer el archivo JSON existente
        with open(json_path, 'r') as file:
            data = json.load(file)
    # Verificar si el contenido es una lista o un diccionario
        if isinstance(data, list):
            for item in data:
                item['Tiempo Neto de Trabajo Repetitivo'] = TNTR
                item['Tiempo Neto del Ciclo'] = TNC
        elif isinstance(data, dict):
            data['Tiempo Neto de Trabajo Repetitivo'] = TNTR
            data['Tiempo Neto del Ciclo'] = TNC
        else:
            raise ValueError("El contenido del archivo JSON no es ni una lista ni un diccionario")

        # Guardar el JSON actualizado
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("El JSON se ha actualizado con TNTR y TNC.")
    except Exception as e:
        print(f"Error al procesar el archivo JSON o al calcular TNTR/TNC: {e}")