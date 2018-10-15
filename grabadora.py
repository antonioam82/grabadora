import pyaudio
import wave
from VALID import ns,OKI
import subprocess

FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100
CHUNK=1024

while True:
    duracion=OKI(input("Introduzca la duración de la grabación: "))


    audio=pyaudio.PyAudio()

    stream=audio.open(format=FORMAT,channels=CHANNELS,
                      rate=RATE, input=True,
                      frames_per_buffer=CHUNK)

    print("recording...")
    frames=[]

    for i in range(0, int(RATE/CHUNK*duracion)):
        data=stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    archivo=(input("Introduzca nombre del archivo a crear: ")+".wav")
    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    ver=ns(input("Desea reproducir el audio creado?: "))
    if ver=="s":
        import os
        os.system(archivo)

    conti=ns(input("¿Desea continuar?: "))
    if conti=="n":
        break
    else:
        subprocess.call(["cmd.exe","/C","cls"])
