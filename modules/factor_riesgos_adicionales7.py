import json
from modules.factor_posturas_movimientos6 import *
from config import JSON_FOLDER

def calculate_additional_risks(actividad):
    """
    Calcula el Factor de Riesgos Adicionales (FC) basado en los riesgos adicionales del JSON proporcionado.
    """
    # Definir criterios para calcular el FC
    # Ejemplo: Puedes tener varios campos que influyen en el FC
    #puntaje_fso = actividad["puntaje_fso",0] #json_data.get('RiesgoAdicional1', 2)
    #puntaje_ffm = actividad["puntaje_ffm",32]
    puntaje_fso = actividad["puntaje_fso"]  # Usamos .get para obtener el valor o un valor por defecto
    puntaje_ffm = actividad["puntaje_ffm"]  # Usamos .get para obtener el valor o un valor por defecto
    
    # Ejemplo de fórmula para el FC
    fc = puntaje_fso + puntaje_ffm 

    
    return fc

def get_most_recent_file(json_folder, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    import os
    import glob
    list_of_files = glob.glob(os.path.join(json_folder, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {json_folder}.")
    return max(list_of_files, key=os.path.getmtime)

def factor_ries_adi(actividad):
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
    print(data)
    # Calcular el FC
    fc = calculate_additional_risks(actividad)

    # Añadir el cálculo al JSON
    data['Factor de Riesgos Adicionales'] = fc

    # Guardar el JSON actualizado
    '''updated_json_path = json_path.replace('.json', '_fc.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Riesgos Adicionales (FC) y guardado en {updated_json_path}.")''' 
    # Guardar el JSON actualizado (sobrescribiendo el archivo existente)
    with open(json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Riesgos Adicionales (FC) y guardado en {json_path}.")