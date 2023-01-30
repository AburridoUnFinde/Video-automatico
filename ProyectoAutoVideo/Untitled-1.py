# Crear videos automaticos con python

import os
import io
import cv2
import numpy as np
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.editor import *

# Lee el guion.txt y separalo por palabras
def leer_guion(guion_file):
    with io.open(guion_file, "r", encoding="utf-8") as f:
        return f.readlines()
    
# Muesta las palabras separadas en la consola    
def separar_guion(guion_lines):
    guion = "\n".join(guion_lines)
    fragmentos = guion.strip().split("\n\n")
    return fragmentos
print(separar_guion(leer_guion("guion.txt")))

# Lee la carpeta de imagenes y muestra los nombres de las imagenes
def leer_imagenes(imagenes_folder):
    lista = []
    for file in os.listdir(imagenes_folder):
        if file.endswith(".jpg") or file.endswith(".gif") or file.endswith(".png")  or file.endswith(".jpeg")   or file.endswith(".jfif")   or file.endswith(".pjpeg")   or file.endswith(".pjp")   or file.endswith(".svg")   or file.endswith(".webp")   or file.endswith(".bmp")   or file.endswith(".ico")   or file.endswith(".cur")   or file.endswith(".tif")   or file.endswith(".tiff")   or file.endswith(".avif")   or file.endswith(".apng") or file.endswith(".mp4"):
            lista.append(file)
    print("Archivos leídos:", lista)
    return lista

# Asocia el guion con las imagenes
# Crear diccionario de asociaciones
def asociar_guion_imagenes(guion_file, imagenes_folder):
    guion_lines = leer_guion(guion_file)
    fragmentos = separar_guion(guion_lines)
    imagenes = leer_imagenes(imagenes_folder)
    
    asociaciones = {}
    for fragmento in fragmentos:
        for nombre_archivo in imagenes:
            if fragmento.lower() in nombre_archivo.lower():
                asociaciones[fragmento] = nombre_archivo
                break
    print("Diccionario de asociaciones:", asociaciones)
    
    # Mostrar fragmentos sin contenido asociado                
    fragmentos_sin_contenido = [f for f in fragmentos if f not in asociaciones]
    if fragmentos_sin_contenido:
        print("Los siguientes fragmentos del guion no tienen contenido asociado:")
        for f in fragmentos_sin_contenido:
            print(f)
            
    return asociaciones

ruta = r"C:\ProyectoAutoVideo\imagenes"
asociaciones = asociar_guion_imagenes("guion.txt", ruta)

# Unir asociaciones en un video mp4

def crear_video(asociaciones, video_file):
    clips = []
    for fragmento, archivo in asociaciones.items():
        if archivo.endswith('.png') or archivo.endswith('.jpg') or archivo.endswith('.gif') or archivo.endswith('.jpeg') or archivo.endswith('.jfif') or archivo.endswith('.pjpeg') or archivo.endswith('.pjp') or archivo.endswith('.svg') or archivo.endswith('.webp') or archivo.endswith('.bmp') or archivo.endswith('.ico') or archivo.endswith('.cur') or archivo.endswith('.tif') or archivo.endswith('.tiff') or archivo.endswith('.avif') or archivo.endswith('.mp4'):
            clip = mp.ImageClip(archivo)
            clip = clip.set_duration(5)
            clip = clip.set_start(0)
            clip = clip.set_end(5)
            clip = clip.set_fps(30)
        elif archivo.endswith('.mp4'):
            clip = mp.VideoFileClip(archivo)
        else:
            print(f"El formato de archivo {archivo} no es compatible.")
            continue
        clips.append(clip)
    video = mp.concatenate_videoclips(clips)
    try:
        video.write_videofile(video_file, fps=30)
    except Exception as e:
        print("Error al crear el video:", e)

# Unir asociaciones en un video mp4 

  # código para escribir en el archivo
crear_video(asociaciones, "video_final.mp4")

