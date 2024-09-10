import json
from modules.factor_frecuencia4 import *
from config import JSON_FOLDER, VIDEO_MARCADO_FOLDER

def get_most_recent_file(json_folder, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    import os
    import glob
    list_of_files = glob.glob(os.path.join(json_folder, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {json_folder}.")
    return max(list_of_files, key=os.path.getmtime)

def factor_fuer(actividad):
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
    # Calcular el FFz
    ffz = actividad["puntaje_acciones_fuerza"] #calcular_ffz(acciones)

    # Añadir el cálculo al JSON
    data['Factor de Fuerza'] = ffz

    # Guardar el JSON actualizado
    with open(json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

