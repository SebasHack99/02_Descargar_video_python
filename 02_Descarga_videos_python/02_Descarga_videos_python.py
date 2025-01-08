import os
import tkinter as tk
from tkinter import simpledialog

from pytube import YouTube


# Función para obtener el enlace del video mediante una ventana de entrada
def obtener_enlace():
    # Crear una ventana raíz
    root = tk.Tk()

    # Ocultar la ventana raíz
    root.withdraw()

    # Mostrar el cuadro de diálogo para ingresar texto
    url = simpledialog.askstring("Ingresar enlace", "Por favor ingrese el enlace del video de YouTube:")

    # Cerrar la ventana raíz después de obtener el enlace
    root.destroy()

    return url

# Carpeta donde se guardarán los videos descargados
folder_path = r'D:\01_Emprendimiento\01_Arca_oexdi\04_Mini_projectos\01_L.Python\02_Descarga_videos_python'
output_folder = os.path.join(folder_path, "videos")
os.makedirs(output_folder, exist_ok=True)

try:
    # Obtener el enlace del video usando la función definida
    url = obtener_enlace()

    if url:
        # Descargar el video desde YouTube
        yt = YouTube(url)
        stream = yt.streams.first()
        stream.download(output_path=output_folder)

        print("Descarga completada en:", output_folder)
    else:
        print("No se proporcionó un enlace válido.")
except Exception as e:
    print(f"Ocurrió un error: {e}")