import os
import shutil
import re
import spacy

# Cargar el modelo de procesamiento de texto de Spacy
nlp = spacy.load("en_core_web_sm")

def obtener_nombre_artista_titulo(nombre_archivo):
    # Aplicar procesamiento de texto para obtener entidades (por ejemplo, nombres de personas y sustantivos)
    doc = nlp(nombre_archivo)
    
    # Inicializar artista y título
    artista = ""
    titulo = ""
    
    # Iterar sobre las entidades en el texto
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not artista:
            artista = ent.text
        elif ent.label_ == "NORP" and not artista:
            artista = ent.text
        elif ent.label_ == "WORK_OF_ART" and not titulo:
            titulo = ent.text

    return artista, titulo

def copiar_y_renombrar_videos(carpeta_origen, carpeta_destino, genero):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    archivos = os.listdir(carpeta_origen)
    patron_video = re.compile(r'.*\.(mp4|avi|mkv|mov)$', re.IGNORECASE)
    contador = 1

    for archivo in archivos:
        ruta_completa_origen = os.path.join(carpeta_origen, archivo)

        if os.path.isfile(ruta_completa_origen) and patron_video.match(archivo):
            nombre_sin_extension, extension = os.path.splitext(archivo)
            
            # Obtener el artista y el título del nombre del archivo
            artista, titulo = obtener_nombre_artista_titulo(nombre_sin_extension)
            
            # Construir el nuevo nombre del archivo
            nuevo_nombre = f"{genero}_{artista}_{titulo}{extension}"
            nuevo_nombre_completo_destino = os.path.join(carpeta_destino, nuevo_nombre)

            try:
                shutil.copy2(ruta_completa_origen, nuevo_nombre_completo_destino)
                print(f"¡Copia exitosa de {archivo} como {nuevo_nombre}!\n")
            except Exception as e:
                print(f"Error al copiar {archivo}: {e}\n")

            contador += 1

if __name__ == "__main__":
    carpeta_origen = input("Ingrese la ruta de la carpeta de origen: ").strip()
    carpeta_destino = input("Ingrese la ruta de la carpeta de destino: ").strip()
    genero = input("Ingrese el género: ").strip()

    copiar_y_renombrar_videos(carpeta_origen, carpeta_destino, genero)
