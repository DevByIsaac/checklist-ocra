import json
from modules.factor_frecuencia4 import *
from config import JSON_FOLDER, VIDEO_MARCADO_FOLDER

""" def calcular_ffz(acciones):
    puntuacion_total = 0
    
    for accion in acciones:
        esfuerzo = accion['esfuerzo_cr10']
        duracion = accion['duracion']
        
        if esfuerzo in [3, 4]:  # Fuerza Moderada
            if duracion == "1/3 del tiempo":
                puntuacion_total += 2
            elif duracion == "50% del tiempo":
                puntuacion_total += 4
            elif duracion == "> 50% del tiempo":
                puntuacion_total += 6
            elif duracion == "Casi todo el tiempo":
                puntuacion_total += 8
                
        elif esfuerzo in [5, 6]:  # Fuerza Intensa
            if duracion == "2 seg. cada 10 min.":
                puntuacion_total += 4
            elif duracion == "1% del tiempo":
                puntuacion_total += 8
            elif duracion == "5% del tiempo":
                puntuacion_total += 16
            elif duracion == "> 10% del tiempo":
                puntuacion_total += 24
        
        elif esfuerzo >= 7:  # Fuerza Casi Máxima
            if duracion == "2 seg. cada 10 min.":
                puntuacion_total += 6
            elif duracion == "1% del tiempo":
                puntuacion_total += 12
            elif duracion == "5% del tiempo":
                puntuacion_total += 24
            elif duracion == "> 10% del tiempo":
                puntuacion_total += 32
    
    return puntuacion_total
 """
""" def obtener_acciones_predeterminadas(actividad):
    acciones = [
        {'esfuerzo_cr10': actividad["puntaje_acciones_fuerza"], 'duracion': "1/3 del tiempo"},
        #{'esfuerzo_cr10': 4, 'duracion': "50% del tiempo"},
        #{'esfuerzo_cr10': 5, 'duracion': "2 seg. cada 10 min."},
        #{'esfuerzo_cr10': 6, 'duracion': "1% del tiempo"},
        #{'esfuerzo_cr10': 7, 'duracion': "5% del tiempo"},
        #{'esfuerzo_cr10': 8, 'duracion': "> 10% del tiempo"}
    ]
    #acciones = [{'esfuerzo_cr10': actividad["puntaje_acciones_fuerza"]}]
    return acciones """

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

    # Intentar extraer acciones del JSON
    #acciones = data.get('acciones_fuerza', None)

    # Si no están presentes en el JSON, usar acciones predeterminadas
    """ if acciones is None:
        print("No se encontraron acciones de fuerza en el archivo JSON. Usando valores predeterminados.")
        acciones = obtener_acciones_predeterminadas()
 """
    # Calcular el FFz
    ffz = actividad["puntaje_acciones_fuerza"] #calcular_ffz(acciones)

    # Añadir el cálculo al JSON
    data['Factor de Fuerza'] = ffz

    # Guardar el JSON actualizado
    with open(json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Fuerza y guardado en {json_path}.")