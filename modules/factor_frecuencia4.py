# Factor de frecuencia
import json
from modules.factor_recuperacion3 import *
def calcular_ff(atd, ate):
    """
    Calcula el Factor de Frecuencia (FF) basado en las puntuaciones ATD y ATE.
    
    :param atd: Puntuación de Acciones Técnicas Dinámicas
    :param ate: Puntuación de Acciones Técnicas Estáticas
    :return: Puntuación del Factor de Frecuencia (FF)
    """
    return max(atd, ate)

def get_most_recent_file(json_folder, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    import os
    import glob
    list_of_files = glob.glob(os.path.join(json_folder, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {json_folder}.")
    return max(list_of_files, key=os.path.getmtime)

def factor_fre(actividad):
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
    # Definir valores predeterminados para ATD y ATE
    valor_atd = actividad["puntaje_atd"]   # Valor fijo de ejemplo para Acciones Técnicas Dinámicas   
    valor_ate = actividad["puntaje_ate"] # Valor fijo de ejemplo para Acciones Técnicas Estáticas

    # Intentar extraer puntuaciones del JSON, sino usar valores predeterminados
    atd = data.get('AccionesTecnicasDinámicas', valor_atd)
    ate = data.get('AccionesTecnicasEstáticas', valor_ate)
    # Calcular el FF
    ff = calcular_ff(atd, ate)

    # Añadir el cálculo al JSON
    data['FF'] = ff

    with open(json_path, 'w') as file:
        json.dump(data_list, file, indent=4)