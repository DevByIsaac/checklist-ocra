import os
class Config:
    DB_NAME = 'tesis-checklist-ocra'
    DB_USER = 'postgres'
    DB_PASSWORD = '12345'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    SECRET_KEY = 'key_ocra_2024'

STATIC_FOLDER = 'static'
JSON_FOLDER = os.path.join(STATIC_FOLDER, 'json')
VIDEO_MARCADO_FOLDER = os.path.join(STATIC_FOLDER, 'video_marcado')
