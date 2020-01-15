#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import Tk,Label,Button,Frame,filedialog,Entry,StringVar,messagebox
import glob
import pyaudio
import os
import wave
import threading

grabando=False
reproduciendo=False
CHUNK=1024
data=""
stream=""
audio=pyaudio.PyAudio() 
f=""
contador=0
contador1=0
contador2=0

ventana = Tk()
ventana.title('Grabadora Audio WAV')
directorio_actual=StringVar()

def clear_contador():
    global contador,contador1,contador2
    contador=0
    contador1=0
    contador2=0

def dire():
    directorio_actual.set(os.getcwd())

def iniciar():
    global grabando
    global proceso
    global act_proceso
    clear_contador()
    audio=pyaudio.PyAudio()
    bloqueo('disabled')
    grabando=True
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    act_proceso=True
    archivo="grabacion.wav"
    t1=threading.Thread(target=grabacion, args=(FORMAT,CHANNELS,RATE,CHUNK,audio,archivo))
    t=threading.Thread(target=cuenta)
    t1.start()
    t.start()

def formato(c):
    if c<10:
        c="0"+str(c)
    return c
    
def cuenta():
    global proceso
    global contador,contador1,contador2
    time['text'] = str(formato(contador1))+":"+str(formato(contador2))+":"+str(formato(contador))
    contador+=1
    if contador==60:
        contador=0
        contador2+=1
    if contador2==60:
        contador2=0
        contador1+=1
    proceso=time.after(1000, cuenta)

def abrir():
    global data
    global stream
    global f
    global reproduciendo
    clear_contador()
    audio=pyaudio.PyAudio()
    open_archive=filedialog.askopenfilename(initialdir = "/",
                 title = "Seleccione archivo",filetypes = (("wav files","*.wav"),
                 ("all files","*.*")))
    if open_archive!="":
        try:
            reproduciendo=True
            f = wave.open(open_archive,"rb")
            stream = audio.open(format = audio.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),
                        output = True)
            data = f.readframes(CHUNK)
            bloqueo('disabled')
            t=threading.Thread(target=cuenta)
            t.start()
            t2=threading.Thread(target=reproduce)
            t2.start()
        except:
            messagebox.showwarning("ERROR","No se pudo abrir al archivo especificado.")
            reproduciendo=False

def reproduce():
    global data
    global stream
    global f
    
    while data and reproduciendo==True:  
        stream.write(data)  
        data = f.readframes(CHUNK)  
 
    stream.stop_stream()  
    stream.close()  
 
    audio.terminate()
    time.after_cancel(proceso)
    #print("FIN")
    bloqueo('normal')

def bloqueo(s):
    btnIniciar.config(state=s)
    btnDir.config(state=s)
    btnAbrir.config(state=s)
    
def parar():
    global grabando
    global reproduciendo
    if grabando==True:
        grabando=False
        time.after_cancel(proceso)
        clear_contador()
    elif reproduciendo==True:
        reproduciendo=False
    bloqueo('normal')

def direc():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
        dire()

def grabacion(FORMAT,CHANNELS,RATE,CHUNK,audio,archivo):
    
    stream=audio.open(format=FORMAT,channels=CHANNELS,
                          rate=RATE, input=True,
                          frames_per_buffer=CHUNK)

    frames=[]

    #print("GRABANDO")
    while grabando==True:
        data=stream.read(CHUNK)
        frames.append(data)
    #print("fin")

    #DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    grabs = glob.glob('*.wav')

    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
    count=0
    for i in grabs:
        if "grabacion" in i:
            count+=1
    if count>0:
        archivo="grabacion"+"("+str(count)+")"+".wav"
        
    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

dire()
time = Label(ventana, fg='green', width=20, text="00:00:00", bg="black", font=("","30"))
time.place(x=10,y=20)
ventana.geometry("488x97")
 
btnIniciar=Button(ventana, fg='blue',width=16, text='Grabar', command=iniciar)
btnIniciar.place(x=122,y=71)
btnParar=Button(ventana, fg='blue', width=16, text='Parar', command=parar)
btnParar.place(x=244,y=71)
btnDir=Button(ventana, text="Carpeta",width=16,command=direc)
btnDir.place(x=0,y=71)
btnAbrir=Button(ventana, text="Abrir",width=16,command=abrir)
btnAbrir.place(x=366,y=71)
etDir=Entry(ventana,width=77,bg="lavender",textvariable=directorio_actual)
etDir.place(x=10,y=0)
 
ventana.mainloop()



