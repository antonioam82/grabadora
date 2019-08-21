#EJEMPLO DE GRABADORA DE SONIDO CON "pyaudio".
#IMPORTAMOS LIBRERIAS NECESARIAS
import pyaudio
import wave
from VALID import ns, OKI
import os

def nuevo_directorio():
    while True:
        nd = input("Directorio: ")
        if os.path.isdir(nd):
            os.chdir(nd)
            break
        else:
            print("RUTA NO VÁLIDA")
        
def archiv():
    while True:
        archiv = input("Introduzca nombre del archivo: ")
        archivo = (archiv+".wav")
        if archivo in os.listdir():
            elim = ns(input("Ya existe un archivo con ese nombre, ¿Desea sobreescribirlo?: "))
            if elim=="s":
                break
            else:
                continue
        else:
            break
    return archivo

nuevo_directorio()

while True:
    #DEFINIMOS PARAMETROS
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    CHUNK=1024

    #INICIAMOS "pyaudio"
    audio=pyaudio.PyAudio()
    duracion=OKI(input("Indique duracion, en segundos, de la grabación: "))

    #INICIAMOS GRABACIÓN
    stream=audio.open(format=FORMAT,channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("grabando...")
    frames=[]

    for i in range(0, int(RATE/CHUNK*duracion)):
        data=stream.read(CHUNK)
        frames.append(data)
    print("grabación terminada")

    #DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
    archivo = archiv()
    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    conti=ns(input("¿Desea continuar?: "))
    if conti=="n":
        break
