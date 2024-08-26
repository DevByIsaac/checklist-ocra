# Factor de Recuperación
import json
import re
from modules.tiempo_neto2 import *
from config import JSON_FOLDER

def get_most_recent_file(json_folder, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    list_of_files = glob.glob(os.path.join(json_folder, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {json_folder}.")
    return max(list_of_files, key=os.path.getmtime)

def calculate_fr(pauses, lunch_break_duration, shift_duration):
    """
    Cálculo de puntuación del FR basado en la Tabla 1.
    """
    num_pauses = len(pauses)
    is_lunch_break_present = lunch_break_duration > 0

    if is_lunch_break_present and lunch_break_duration >= 8:
        if shift_duration >= 60:
            return 0  # Ideal
        elif num_pauses >= 4:
            return 2
    elif is_lunch_break_present and num_pauses >= 3:
        return 3
    elif num_pauses >= 2:
        return 4
    elif num_pauses == 1:
        return 6
    else:
        return 10  # Sin pausas adecuadas

def convert_to_minutes(time_str):
    """Convierte una cadena de tiempo en formato 'Xh Ym' a minutos y valida el formato."""
    time_str = time_str.strip()
    if re.match(r'^\d+h \d+m$', time_str):
        hours, minutes = time_str.split('h')
        minutes = minutes.replace('m', '').strip()
        return int(hours.strip()) * 60 + int(minutes)
    elif re.match(r'^\d+h$', time_str):
        hours = time_str.replace('h', '').strip()
        return int(hours) * 60
    elif re.match(r'^\d+m$', time_str):
        minutes = time_str.replace('m', '').strip()
        return int(minutes)
    else:
        raise ValueError("Formato de tiempo no válido. Use 'Xh Ym', 'Xh' o 'Ym'.")

def get_input(prompt):
    """Solicita al usuario un valor y maneja errores de entrada."""
    while True:
        try:
            value = input(prompt)
            return convert_to_minutes(value)
        except ValueError as e:
            print(f"Error: {e}. Inténtalo de nuevo con el formato correcto.")

def factor_recu(empleado, actividad):
    # Datos de prueba
    pauses = actividad.get("num_pauses", [10])  # Usa 10 como valor predeterminado si el dato no está disponible
    lunch_break_duration = actividad.get("lunch_break_duration", 30)  # Valor predeterminado 30 minutos
    shift_duration = actividad["duracion_turno"]  # Esta clave parece estar presente, así que la mantenemos como está
    #num_pauses = actividad.get("num_pauses", 0)

    # Ruta del archivo JSON
    json_path = get_most_recent_file(JSON_FOLDER, '.json')

    # Leer el archivo JSON
    with open(json_path, 'r') as file:
        data_list = json.load(file)

    # Verificar si data_list es una lista y si no está vacía
    if not isinstance(data_list, list) or len(data_list) == 0:
        raise ValueError("El archivo JSON no contiene una lista válida o está vacío.")

    # Tomar el primer objeto de la lista
    data = data_list[0]
    # Calcular el FR
    # Extraer datos del JSON
    # Los datos se sobreescriben con los valores ingresados por el usuario
    # Calcular el FR
    fr = calculate_fr(pauses, lunch_break_duration, shift_duration)

    # Añadir el cálculo al JSON
    data['Factor de Recuperacion'] = fr

    # Guardar el JSON actualizado
    '''updated_json_path = json_path.replace('.json', 'FR.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)'''
    # Guardar el JSON actualizado (sobrescribiendo el archivo existente)
    with open(json_path, 'w') as file:
        json.dump(data_list, file, indent=4)
    print(f"El JSON se ha actualizado con el Factor de Recuperación y guardado en {json_path}.")
    #print(f"El JSON se ha actualizado con el Factor de Recuperación y guardado en {updated_json_path}.")