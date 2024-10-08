import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import io

# Título de la aplicación
st.title("Cargar un archivo de audio desde tu PC y transcribirlo")

# Instrucciones para el usuario
st.write("Selecciona un archivo de audio con extensión .ogg para cargarlo.")

# Selector de archivos (aceptando solo archivos .ogg)
archivo_ogg = st.file_uploader("Elige un archivo de audio", type=["ogg"])

# Verificar si el archivo fue cargado
if archivo_ogg is not None:
    # Mostrar detalles del archivo
    file_details = {"FileName": archivo_ogg.name, "FileType": archivo_ogg.type}
    st.write(file_details)

    # Procesar el archivo .ogg y convertirlo a .wav en memoria
    st.audio(archivo_ogg, format='audio/ogg')

    # Leer el archivo OGG desde el objeto en memoria
    audio = AudioSegment.from_ogg(archivo_ogg)

    # Crear un buffer de memoria para almacenar el archivo WAV
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)  # Ir al principio del archivo para que pueda ser leído

    # Inicializar el reconocedor de voz
    recognizer = sr.Recognizer()

    # Transcribir el archivo de audio desde el buffer en memoria
    try:
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
        
        # Usar Google API para la transcripción
        text = recognizer.recognize_google(audio_data, language="es-ES")
        st.write("Transcripción: ")
        st.write(text)

    except sr.UnknownValueError:
        st.write("Lo siento, no pude entender el audio.")
    except sr.RequestError as e:
        st.write(f"Error en la solicitud; {e}")

else:
    st.write("Por favor, carga un archivo de audio.")

