import streamlit as st
import speech_recognition as sr
import soundfile as sf
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

    # Procesar el archivo de audio .ogg
    st.audio(archivo_ogg, format='audio/ogg')

    # Inicializar el reconocedor de voz
    recognizer = sr.Recognizer()

    try:
        # Leer el archivo cargado en memoria como un flujo de bytes
        archivo_bytes = archivo_ogg.read()

        # Convertir el archivo OGG a WAV usando soundfile
        with io.BytesIO(archivo_bytes) as ogg_io:
            data, samplerate = sf.read(ogg_io)
            wav_io = io.BytesIO()
            sf.write(wav_io, data, samplerate, format='WAV')
            wav_io.seek(0)

        # Usar speech_recognition para manejar el archivo WAV
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
    except Exception as e:
        st.write(f"Ocurrió un error al procesar el archivo de audio: {e}")

else:
    st.write("Por favor, carga un archivo de audio.")
