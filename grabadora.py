from tkinter import Tk,Label,Button,Frame,filedialog
import pyaudio
import os
import wave

import threading

def iniciar(contador=0):
    global grabando
    global proceso
    grabando=True
    time['text'] = contador
    
    t1=threading.Thread(target=grabacion)
    t1.start()
    proceso=time.after(1000, iniciar, (contador+1))
 
def parar():
    global grabando
    global proceso
    grabando=False
    time.after_cancel(proceso)

def direc():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)

def grabacion():
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    CHUNK=1024
    archivo="grabacion.wav"

    audio=pyaudio.PyAudio()

    stream=audio.open(format=FORMAT,channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames=[]

    while grabando==True:
        data=stream.read(CHUNK)
        frames.append(data)
    print("fin")

    #DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

ventana = Tk()
ventana.title('Grabadora')

time = Label(ventana, fg='red', width=20, font=("","30"))
time.pack()
ventana.geometry("470x77")
 
frame=Frame(ventana)
btnIniciar=Button(frame, fg='blue',width=21, text='Iniciar', command=iniciar)
btnIniciar.grid(row=1, column=1)
btnParar=Button(frame, fg='blue', width=21, text='Parar', command=parar)
btnParar.grid(row=1, column=2)
btnDir=Button(frame, text="Directorio",width=21,command=direc)
btnDir.grid(row=1,column=0)
frame.pack()
 
ventana.mainloop()
