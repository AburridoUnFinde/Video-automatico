# codigo de un programa al que yo le de un guion de youtube, y puda crear un video, con pedazos de video de una carpeta
# y con la musica de una carpeta, y con la imagen de una carpeta, y con el texto de un archivo de texto

import os
import io
from moviepy import editor as mp




# Leer los audios de la carpeta musica y almacenarlos en una lista
def leer_audios(musica):
    lista = []
    for file in os.listdir(musica):
        if file.endswith(".mp3"):
            lista.append(file)
    print("Archivos de musica leídos:", lista)
    return lista

# Leer las imagenes de la carpeta y almacenarlos en una lista
    
imagenes = {
    'chips.gif': 'Fragmento 1: Introducción a los chips',
    'fabrica.jpg': 'Fragmento 2: La fabricación de los chips',
    '5G.gif': 'Fragmento 3: La tecnología 5G y los chips',
}

def leer_imagenes(imagenes, guion):
    resultado = {1}
    for file in os.listdir(imagenes):
        try:
         if file.endswith(".jpg") or file.endswith(".gif"):
            for k, v in imagenes.items():
                if v in guion.values() and k == file:
                    
                    nombre_imagen = k
                    fragmento = v
                    resultado[fragmento] = os.path.join(imagenes, file)
                    print(f" - {k}: {v}")
        except Exception as e:
            print("Error:", e)
    return resultado



# Leer un guion y retornar una lista con todos los fragmentos:
def leer_guion(guion):
    with io.open(guion, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# Separar los fragmentos del guion
def separar_guion(guion):
    guion = '\n'.join(guion)
    fragmentos = guion.strip().split("\n\n")
    return fragmentos

# Asociar guion con el video correspondiente
def asociar_guion(guion, videos):
    resultado = {2}
    for fragmento in guion:
        for nombre_video, descripcion_fragmento in videos.items():
            try:
             if fragmento.startswith(descripcion_fragmento):
                resultado[nombre_video] = fragmento
                break
            except Exception as e:
                print("Error:", e)
    return resultado

# Uso
guion = leer_guion("guion.txt")
fragmentos = separar_guion(guion)

# Asociar guion con el video correspondiente
videos = {
    'chips.mp4': 'Fragmento 1: Introducción a los chips',
    'fabrica.mp4': 'Fragmento 2: La fabricación de los chips',
    '5G.mp4': 'Fragmento 3: La tecnología 5G y los chips',
}

def asociar_guion(fragmentos, videos):
    resultado = {}
    for fragmento in fragmentos:
        for nombre_video, nombre_fragmento in videos.items():
            if nombre_fragmento in fragmento:
                resultado[nombre_video] = fragmento
                break
    return resultado

try:
    resultado = asociar_guion(fragmentos, videos)
except Exception as e:
    print("Error:", e)
else:
    print(resultado)


# Recorrer la lista de videos y los fragmentos de texto, y usar OpenCV y moviepy para unir cada fragmento de video con el texto correspondiente.
def crear_video(lista_videos, lista_textos, lista_audios, lista_imagenes):
    # Crear la lista de clips para el video
    clips = []
    # Recorrer la lista de videos y textos
    for i in range(len(lista_videos)):
        # Obtener el path del video o imagen
        path_video_o_imagen = lista_videos[i] if lista_videos[i].endswith('.mp4') else lista_imagenes[i]
        # Verificar si el archivo existe
        if os.path.exists(path_video_o_imagen):
            # Crear el clip
            clip = mp.VideoFileClip(path_video_o_imagen)
        else:
            # Si no existe, buscar el otro tipo de archivo
            path_video_o_imagen = lista_videos[i] if lista_videos[i].endswith('.gif') else lista_imagenes[i]
            # Verificar si existe
            if os.path.exists(path_video_o_imagen):
                # Crear el clip
                clip = mp.ImageClip(path_video_o_imagen)
            else:
                # Si no existe ningún archivo, lanzar una excepción
                raise Exception(f'No se encontró ningún archivo en {lista_videos[i]} ni en {lista_imagenes[i]}')
        # Crear el texto
        texto = mp.TextClip(lista_textos[i], fontsize=70, color='white')
        # Unir el clip con el texto
        clip = mp.CompositeVideoClip([clip, texto])
        # Añadir el clip a la lista de clips
        clips.append(clip)
    # Unir todos los clips
    
    video = mp.concatenate_videoclips(clips)
    # Crear el audio
    audio = mp.AudioFileClip(lista_audios[0])
    # Unir el audio con el video
    video = video.set_audio(audio)
    
    # Guardar el video
    video.write_videofile("video.mp4")