import os
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError, VideoUnavailable, LiveStreamError

def obtener_enlace():
    """Solicita al usuario un enlace de YouTube mediante un diálogo."""
    url = simpledialog.askstring("Ingresar enlace", "📎 Ingresa el enlace del video de YouTube:")
    return url

def seleccionar_carpeta_destino():
    """Permite al usuario seleccionar una carpeta de destino para el video descargado."""
    folder_selected = filedialog.askdirectory(title="📁 Selecciona la carpeta donde guardar el video")
    if not folder_selected:  # Si no se seleccionó una carpeta, mostramos advertencia
        messagebox.showwarning("Advertencia", "❌ No se seleccionó una carpeta. Se guardará en la carpeta predeterminada.")
        folder_selected = os.getcwd()  # Si no selecciona, se guarda en la carpeta actual
    return folder_selected

def descargar_video(url, carpeta_destino):
    """Descarga el primer stream de un video de YouTube o maneja una lista de reproducción."""
    try:
        print(f"🔗 URL proporcionada: {url}")
        # Verifica si la URL corresponde a una lista de reproducción
        if 'playlist' in url:
            return descargar_lista_reproduccion(url, carpeta_destino)
        
        yt = YouTube(url)
        print(f"🖥️ Conectando al video: {yt.title}")
        stream = yt.streams.get_highest_resolution()  # Mejor resolución disponible
        print(f"📥 Iniciando descarga del video {yt.title}...")
        stream.download(output_path=carpeta_destino)
        return f"✅ Video descargado con éxito: {yt.title}"
    except RegexMatchError:
        raise ValueError("❌ URL no válida de YouTube. Verifique que la URL esté correctamente formateada.")
    except VideoUnavailable:
        raise ValueError("❌ El video no está disponible o ha sido eliminado.")
    except LiveStreamError:
        raise ValueError("❌ El video es un livestream y no se puede descargar.")
    except Exception as e:
        raise e

def descargar_lista_reproduccion(url, carpeta_destino):
    """Descarga todos los videos de una lista de reproducción de YouTube."""
    try:
        playlist = Playlist(url)
        print(f"Descargando videos de la lista: {playlist.title}")
        
        for video_url in playlist.video_urls:
            print(f"🔄 Descargando: {video_url}")
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=carpeta_destino)
            print(f"✅ Video descargado: {yt.title}")
        
        return f"✅ Todos los videos de la lista han sido descargados."
    except Exception as e:
        print(f"❌ Error al descargar la lista: {e}")
        return f"❌ Error al descargar la lista: {e}"

def crear_ventana_principal():
    """Crea la ventana principal de la aplicación con diseño visual atractivo."""
    ventana = tk.Tk()
    ventana.title("🎬 Descargador de Videos YouTube")
    ventana.geometry("600x400")
    ventana.config(bg="#263238")  # Fondo oscuro y elegante
    ventana.resizable(False, False)  # No cambiar tamaño de ventana

    # Título en la ventana
    label_titulo = tk.Label(ventana, text="¡Bienvenido al Descargador de Videos!", font=("Helvetica", 16, "bold"), fg="white", bg="#263238")
    label_titulo.pack(pady=30)

    # Instrucción para comenzar
    label_instruccion = tk.Label(ventana, text="Para comenzar, ingresa el enlace del video:", font=("Helvetica", 12), fg="#B0BEC5", bg="#263238")
    label_instruccion.pack(pady=10)

    # Botón para iniciar el proceso
    boton_iniciar = tk.Button(ventana, text="📥 Iniciar Descarga", command=lambda: iniciar_descarga(ventana), font=("Helvetica", 12, "bold"), bg="#FF7043", fg="white", relief="flat", width=20, height=2)
    boton_iniciar.pack(pady=30)

    # Footer con créditos
    footer = tk.Label(ventana, text="Desarrollado por Arca Oexdi", font=("Helvetica", 8), fg="#B0BEC5", bg="#263238")
    footer.pack(side="bottom", pady=10)

    # Mostrar ventana
    ventana.mainloop()

def iniciar_descarga(ventana):
    """Inicia el proceso de descarga y maneja la interacción con el usuario."""
    try:
        # Obtener enlace y carpeta de destino
        url = obtener_enlace()
        if not url:
            messagebox.showwarning("Advertencia", "❌ No se proporcionó un enlace válido.")
            return

        carpeta = seleccionar_carpeta_destino()
        if not carpeta:
            messagebox.showwarning("Advertencia", "❌ No se seleccionó una carpeta de destino.")
            return

        # Usamos os para asegurarnos que la carpeta existe y crearla si es necesario
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Descargar el video
        print("🔄 Descargando video...")
        resultado = descargar_video(url, carpeta)
        messagebox.showinfo("¡Éxito!", resultado)
        print(f"✅ Video(s) descargado(s) en → {carpeta}")

    except ValueError as ve:
        messagebox.showerror("Error de URL", f"{ve}")
        print(f"❌ Error: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al intentar descargar el video:\n{e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_ventana_principal()
