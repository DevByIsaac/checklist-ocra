import json
from modules.factor_fuerza5 import *
from config import JSON_FOLDER, VIDEO_MARCADO_FOLDER

def calculate_posture_movements(json_data):
    """
    Calcula el Factor de Posturas y Movimientos (FP) basado en los ángulos de postura del JSON proporcionado.
    """
    
    def get_posture_score(angle):
        """ Determina la puntuación basada en el ángulo de postura """
        # Asegúrate de que angle no sea None; usa 0 como valor predeterminado si es None
        if angle is None:
            angle = 0
            
        if angle < 45:
            return 1  # Buen rango
        elif angle < 90:
            return 2  # Rango moderado
        elif angle < 135:
            return 4  # Rango alto
        else:
            return 8  # Rango muy alto

    # Obtener las puntuaciones individuales basadas en los ángulos
    ph = get_posture_score(json_data.get('angulo_hombro_izquierdo', 0))
    pc = get_posture_score(json_data.get('angulo_codo_izquierdo', 0))
    pm = get_posture_score(json_data.get('angulo_de_muneca_izquierda', 0))
    pa = get_posture_score(json_data.get('angulo_mano_izquierdo', 0))

    # Obtener las puntuaciones individuales basadas en los ángulos del lado derecho
    ph_r = get_posture_score(json_data.get('angulo_hombro_derecho', 0))
    pc_r = get_posture_score(json_data.get('angulo_codo_derecho', 0))
    pm_r = get_posture_score(json_data.get('angulo_de_muneca_derecha', 0))
    pa_r = get_posture_score(json_data.get('angulo_mano_derecho', 0))

    # Obtener la puntuación para movimientos estereotipados (asumimos que es un campo existente)
    pes = json_data.get('MovimientosEstereotipados', 0)

    # Calcular FP
    #fp = max(ph, pc, pm, pa) + pes

    # Calcular FP tomando el máximo entre todos los ángulos del lado izquierdo y derecho
    fp = max(ph, pc, pm, pa, ph_r, pc_r, pm_r, pa_r) + pes

    return fp
def get_most_recent_file(json_folder, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    import os
    import glob
    list_of_files = glob.glob(os.path.join(json_folder, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {json_folder}.")
    return max(list_of_files, key=os.path.getmtime)

def factor_pos_mov():
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

    # Calcular el FP
    fp = calculate_posture_movements(data)

    # Añadir el cálculo al JSON
    data['Factor de Posturas y Movimientos'] = fp

    # Guardar el JSON actualizado
    '''updated_json_path = json_path.replace('.json', '_fp.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Posturas y Movimientos y guardado en {updated_json_path}.")''' 
    # Guardar el JSON actualizado (sobrescribiendo el archivo existente)
    with open(json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Posturas y Movimientos y guardado en {json_path}.")