import os
import shutil
import re

def copiar_y_renombrar_videos(carpeta_origen, carpeta_destino, genero):
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Obtener la lista de archivos en la carpeta de origen
    archivos = os.listdir(carpeta_origen)

    # Expresión regular para identificar archivos de video (puedes ajustarla según tus necesidades)
    patron_video = re.compile(r'.*\.(mp4|avi|mkv|mov)$', re.IGNORECASE)

    # Contador para el nombre del archivo
    contador = 1

    # Iterar sobre los archivos en la carpeta de origen
    for archivo in archivos:
        ruta_completa_origen = os.path.join(carpeta_origen, archivo)

        # Verificar si es un archivo de video
        if os.path.isfile(ruta_completa_origen) and patron_video.match(archivo):
            # Obtener la extensión del archivo
            _, extension = os.path.splitext(archivo)

            # Construir el nuevo nombre del archivo
            nuevo_nombre = f"{genero}_{input(f'Ingrese nombre para {archivo} sin extensión')}_jerrydi_{contador}{extension}"
            nuevo_nombre_completo_destino = os.path.join(carpeta_destino, nuevo_nombre)

            try:
                # Copiar el archivo a la carpeta de destino y renombrarlo
                shutil.copy2(ruta_completa_origen, nuevo_nombre_completo_destino)
                print(f"¡Copia exitosa de {archivo}!\n")
            except Exception as e:
                print(f"Error al copiar {archivo}: {e}\n")

            # Incrementar el contador
            contador += 1

if __name__ == "__main__":
    carpeta_origen = input("Ingrese la ruta de la carpeta de origen: ").strip()
    carpeta_destino = input("Ingrese la ruta de la carpeta de destino: ").strip()
    genero = input("Ingrese el género: ").strip()

    copiar_y_renombrar_videos(carpeta_origen, carpeta_destino, genero)
