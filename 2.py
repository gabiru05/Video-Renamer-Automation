import os
import shutil
import re
import spacy
import lyricsgenius
import keyboard

# Cargar el modelo de procesamiento de texto de Spacy
nlp = spacy.load("en_core_web_sm")

def limpiar_nombre(nombre):
    # Eliminar términos no deseados y paréntesis
    nombre_limpiado = re.sub(r'(y2mate\.com|y2mate|\(.*\)|\d+p_hd)', '', nombre, flags=re.IGNORECASE)
    # Eliminar espacios duplicados y guiones bajos consecutivos
    nombre_limpiado = re.sub(r'\s+', ' ', nombre_limpiado).strip().replace('_', ' ')
    return nombre_limpiado

def obtener_nombre_artista_titulo(nombre_archivo):
    # Utilizar la API de Genius para buscar información de la canción
    genius = lyricsgenius.Genius("TU_API_KEY_AQUI")  # Reemplaza "TU_API_KEY_AQUI" con tu clave de API de Genius
    
    try:
        cancion = genius.search_song(nombre_archivo)
        
        # Si la API de Genius devuelve resultados
        if cancion:
            return cancion.artist, cancion.title
    except Exception as e:
        print(f"Error al buscar la canción en Genius: {e}")

    # Si la búsqueda falla o no hay resultados, extraer información del nombre del archivo
    # Este es el enfoque por defecto si Genius no proporciona resultados
    nombre_sin_extension, _ = os.path.splitext(nombre_archivo)
    # Dividir el nombre del archivo en palabras y asumir que las primeras dos son artista y título
    partes_nombre = nombre_sin_extension.split('_')
    
    # Obtener el artista y el título del nombre del archivo
    artista = partes_nombre[0] if partes_nombre else ""
    titulo = partes_nombre[1] if len(partes_nombre) > 1 else ""

    return artista, titulo

def copiar_y_renombrar_videos(carpeta_origen, carpeta_destino, genero):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    archivos = os.listdir(carpeta_origen)
    patron_video = re.compile(r'.*\.(mp4|avi|mkv|mov)$', re.IGNORECASE)

    # Contador para enumerar archivos
    contador = 1

    for archivo in archivos:
        ruta_completa_origen = os.path.join(carpeta_origen, archivo)

        if os.path.isfile(ruta_completa_origen) and patron_video.match(archivo):
            nombre_sin_extension, extension = os.path.splitext(archivo)
            
            # Obtener el artista y el título del nombre del archivo utilizando la API de Genius o directamente
            artista, titulo = obtener_nombre_artista_titulo(nombre_sin_extension)
            
            # Limpiar el nombre para eliminar términos no deseados y mejorar la presentación
            artista = limpiar_nombre(artista)
            titulo = limpiar_nombre(titulo)
            
            # Construir el nuevo nombre del archivo con el contador
            nuevo_nombre = f"{genero}_{artista}_{titulo}_{contador}{extension}"
            nuevo_nombre_completo_destino = os.path.join(carpeta_destino, nuevo_nombre)

            try:
                shutil.copy2(ruta_completa_origen, nuevo_nombre_completo_destino)
                print(f"Copiado exitoso: {archivo} -> {nuevo_nombre}")
                # Incrementar el contador
                contador += 1
            except Exception as e:
                print(f"Error al copiar {archivo}: {e}")

        # Verificar si la tecla "L" ha sido presionada para cancelar la ejecución
        if keyboard.is_pressed("l"):
            print("Operación cancelada por el usuario.")
            break

if __name__ == "__main__":
    carpeta_origen = input("Ingrese la ruta de la carpeta de origen: ").strip()
    carpeta_destino = input("Ingrese la ruta de la carpeta de destino: ").strip()
    genero = input("Ingrese el género: ").strip()

    copiar_y_renombrar_videos(carpeta_origen, carpeta_destino, genero)
