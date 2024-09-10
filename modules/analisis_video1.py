import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import os
import datetime 
import json
from modules.tiempo_neto2 import *
from modules.factor_recuperacion3 import *
from modules.factor_frecuencia4 import *
from modules.factor_fuerza5 import *
from modules.factor_posturas_movimientos6 import *
from modules.factor_riesgos_adicionales7 import *
from modules.multiplicador_duracion8 import *
from modules.evaluacion_ocra9 import *
import shutil 
from database import get_actividad_by_empleado_id

def process_video(video_dir, empleado):
    actividad = get_actividad_by_empleado_id(empleado["empleado_id"])
    videos = [video_dir]

    # Inicializar MediaPipe para detección de puntos clave
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    video_path = videos[0]
    static_folder = 'static'
    video_marcado_folder = os.path.join(static_folder, 'video_marcado')
    json_folder = os.path.join(static_folder, 'json')

    # Crea las carpetas si no existen
    if not os.path.exists(video_marcado_folder):
        os.makedirs(video_marcado_folder)
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    # Define la ruta de salida del video
    output_video_folder = video_marcado_folder
    
    #json_folder = 'C:\\Tesis\\TestErgo\\archivos_json'
    video_exportado, json_archivo = draw_keypoints_and_angles(video_path, output_video_folder, json_folder, mp_pose)
    tiempo_neto(empleado, actividad)
    factor_recu(empleado, actividad)
    factor_fre(actividad)
    factor_fuer(actividad)
    factor_pos_mov()
    factor_ries_adi(actividad)
    data_list = multiplicador()
    excel_path = convertir_datafram(data_list)
    return video_exportado, json_archivo, excel_path

def guardar_video_marcado(video_path, video_name):
    # Define la ruta de la carpeta 'video_marcado' dentro de 'static'
    static_folder = 'static'
    video_marcado_folder = os.path.join(static_folder, 'video_marcado')
    
    output_path = os.path.join(video_marcado_folder, video_name)
    # Guarda el video marcado en la carpeta 'video_marcado'
    shutil.copy(video_path, output_path)
    return output_path

def guardar_json(data, json_name):
    # Define la ruta de la carpeta 'json' dentro de 'static'
    static_folder = 'static'
    json_folder = os.path.join(static_folder, 'json')
    
    # Define la ruta completa del archivo JSON
    json_path = os.path.join(json_folder, json_name)
    
    # Guarda el archivo JSON
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    return json_path

def load_videos(video_dir):
    videos = []
    for filename in os.listdir(video_dir):
        if filename.endswith(".mp4"):
            videos.append(os.path.join(video_dir, filename))
    return videos

def guardar_excel(excel_path):
    excel_path()

    return excel_path

# Función para extraer frames de los videos
def extract_frames(video_path, interval=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frames.append(frame)
        count += 1
    cap.release()
    return frames

# Función para calcular el ángulo entre tres puntos
def calculate_angle(a, b, c, d=None):
    if d is None:
        # Calcula el ángulo entre a, b y c
        a = np.array(a)  # Primer punto
        b = np.array(b)  # Segundo punto (vértice)
        c = np.array(c)  # Tercer punto

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360.0 - angle

        return angle
    else:
        # Calcula el ángulo entre a, b, c y d
        a = np.array(a)  # Primer punto
        b = np.array(b)  # Segundo punto (vértice)
        c = np.array(c)  # Tercer punto
        d = np.array(d)  # Cuarto punto

        radians = np.arctan2(d[1] - c[1], d[0] - c[0]) - np.arctan2(b[1] - a[1], b[0] - a[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360.0 - angle

        return angle

# Función para detectar puntos clave usando MediaPipe
def detect_keypoints(video_path, mp_pose):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    keypoints_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        if results.pose_landmarks:
            keypoints = [(lm.x, lm.y, lm.z) for lm in results.pose_landmarks.landmark]
            keypoints_list.append(keypoints)
        else:
            keypoints_list.append([])  # Agregar una lista vacía si no se detectan keypoints

    cap.release()
    pose.close()
    return keypoints_list

def analyze_keypoints(video_path, mp_pose):
    keypoints_list = detect_keypoints(video_path, mp_pose)
    fps = None
    analysis_results = []

    for frame_idx, keypoints in enumerate(keypoints_list):
        second = frame_idx // fps if fps else 0

        if not keypoints:
            analysis_results.append({
                'segundo': second,
                'frame': frame_idx,
                'analisis_video': video_path,
                'angulo_hombro_izquierdo': 0,
                'angulo_del_hombro_derecho': 0,
                'angulo_codo_izquierdo': 0,
                'angulo_codo_derecho': 0,
                'angulo_de_muneca_izquierda': 0,
                'angulo_de_muneca_derecha': 0,
                'angulo_mano_izquierdo': 0,
                'angulo_mano_derecho': 0,
                'posicion_hombro_izquierdo': 0,
                'posicion_hombro_derecho': 0,
                'posicion_codo_izquierdo': 0,
                'posicion_codo_derecho': 0,
                'posicion_muneca_izquierda': 0,
                'posicion_muneca_derecha': 0,
                'posicion_mano_izquierda': 0,
                'posicion_mano_derecha': 0,
                'keypoints': []
            })
            continue

        # Extraer puntos clave izquierdos
        left_shoulder = keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]
        left_hand = keypoints[mp_pose.PoseLandmark.LEFT_INDEX.value]

        # Extraer puntos clave derechos
        right_shoulder = keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        right_wrist = keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_hand = keypoints[mp_pose.PoseLandmark.RIGHT_INDEX.value]

        # Calcular ángulos izquierdos
        left_shoulder_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_elbow_angle = calculate_angle(left_elbow, left_wrist, left_hand)
        left_wrist_angle = calculate_angle(left_elbow, left_wrist, left_hand)
        left_hand_angle = calculate_angle(left_elbow, left_wrist, left_hand)

        # Calcular ángulos derechos
        right_shoulder_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_elbow_angle = calculate_angle(right_elbow, right_wrist, right_hand)
        right_wrist_angle = calculate_angle(right_elbow, right_wrist, right_hand)
        right_hand_angle = calculate_angle(right_elbow, right_wrist, right_hand)

        # Si no se ha establecido aún el FPS, se establece ahora
        if fps is None:
            cap = cv2.VideoCapture(video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            cap.release()

        analysis_results.append({
            'segundo': second,
            'frame': frame_idx,
            'analisis_video': video_path,
            'angulo_hombro_izquierdo': left_shoulder_angle,
            'angulo_del_hombro_derecho': right_shoulder_angle,
            'angulo_codo_izquierdo': left_elbow_angle,
            'angulo_codo_derecho': right_elbow_angle,
            'angulo_de_muneca_izquierda': left_wrist_angle,
            'angulo_de_muneca_derecha': right_wrist_angle,
            'angulo_mano_izquierdo': left_hand_angle,
            'angulo_mano_derecho': right_hand_angle,
            'posicion_hombro_izquierdo': left_shoulder,
            'posicion_hombro_derecho': right_shoulder,
            'posicion_codo_izquierdo': left_elbow,
            'posicion_codo_derecho': right_elbow,
            'posicion_muneca_izquierda': left_wrist,
            'posicion_muneca_derecha': right_wrist,
            'posicion_mano_izquierda': left_hand,
            'posicion_mano_derecha': right_hand,
            'keypoints': keypoints
        })

    return analysis_results, fps

def draw_keypoints_and_angles(video_path, output_video_folder, json_folder, mp_pose):
    analysis_results, fps = analyze_keypoints(video_path, mp_pose)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_video_name = f"{video_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_video_path = os.path.join(output_video_folder, output_video_name)
    json_filename = f"{video_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_path = os.path.join(json_folder, json_filename)

    # Crear carpetas si no existen
    if not os.path.exists(output_video_folder):
        os.makedirs(output_video_folder)
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    # Crear el video marcado
    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    for i in range(len(analysis_results)):
        ret, frame = cap.read()
        if not ret:
            break

        keypoints = analysis_results[i]['keypoints']
        left_shoulder_angle = analysis_results[i]['angulo_hombro_izquierdo']
        right_shoulder_angle = analysis_results[i]['angulo_del_hombro_derecho']
        left_elbow_angle = analysis_results[i]['angulo_codo_izquierdo']
        right_elbow_angle = analysis_results[i]['angulo_codo_derecho']
        left_wrist_angle = analysis_results[i]['angulo_de_muneca_izquierda']
        right_wrist_angle = analysis_results[i]['angulo_de_muneca_derecha']
        left_hand_angle = analysis_results[i]['angulo_mano_izquierdo']
        right_hand_angle = analysis_results[i]['angulo_mano_derecho']

        # Dibujar puntos clave y conexiones con el color original
        if keypoints:
            for j, point in enumerate(keypoints):
                cv2.circle(frame, (int(point[0] * frame.shape[1]), int(point[1] * frame.shape[0])), 5, (0, 255, 0), -1)

                # Añadir texto con información relevante junto a cada punto
                if j == mp_pose.PoseLandmark.LEFT_SHOULDER.value:
                    cv2.putText(frame, f'Angulo del hombro izquierdo: {int(left_shoulder_angle) if left_shoulder_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.RIGHT_SHOULDER.value:
                    cv2.putText(frame, f'Angulo del hombro derecho: {int(right_shoulder_angle) if right_shoulder_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.LEFT_ELBOW.value:
                    cv2.putText(frame, f'Angulo del codo izquierdo: {int(left_elbow_angle) if left_elbow_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.RIGHT_ELBOW.value:
                    cv2.putText(frame, f'Angulo del codo derecho: {int(right_elbow_angle) if right_elbow_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.LEFT_WRIST.value:
                    cv2.putText(frame, f'Angulo de la muneca izquierda: {int(left_wrist_angle) if left_wrist_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.RIGHT_WRIST.value:
                    cv2.putText(frame, f'Angulo de la muneca derecha: {int(right_wrist_angle) if right_wrist_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.LEFT_INDEX.value:
                    cv2.putText(frame, f'Angulo de la mano izquierda: {int(left_hand_angle) if left_hand_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                elif j == mp_pose.PoseLandmark.RIGHT_INDEX.value:
                    cv2.putText(frame, f'Angulo de la mano derecha: {int(right_hand_angle) if right_hand_angle else 0}',
                                (int(point[0] * frame.shape[1]) + 10, int(point[1] * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Guardar el frame en el video marcado
        out.write(frame)

    cap.release()
    out.release()
    
    # Guardar el archivo JSON con los resultados del análisis
    with open(json_path, 'w') as json_file:
        json.dump(analysis_results, json_file, indent=4)
    return output_video_path, json_path
