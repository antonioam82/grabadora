#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import Tk,Label,Button,Frame,filedialog
from tkinter import *
import pyaudio
import os
import wave
import threading

grabando=False
reproduciendo=False
CHUNK=1024
data=""
stream=""
f=""

contador=0
contador1=0
contador2=0

ventana = Tk()
ventana.title('Grabadora Audio')
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
    #global contador,contador1,contador2
    clear_contador()
    audio=pyaudio.PyAudio()
    #btnParar.config(text="Parar Grabación")
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
    #stc=formato(contador)
    #stc1=formato(contador1)
    #stc2=formato(contador2)
    time['text'] = str(formato(contador1))+":"+str(formato(contador2))+":"+str(formato(contador))
    #time['text'] = stc1+":"+stc2+":"+stc 
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
    #global contador, contador1,contador2
    clear_contador()
    audio=pyaudio.PyAudio()
    open_archive=filedialog.askopenfilename(initialdir = "/",
                 title = "Seleccione archivo",filetypes = (("wav files","*.wav"),
                 ("all files","*.*")))
    if open_archive!="":
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

def reproduce():
    global data
    global stream
    global f
    audio=pyaudio.PyAudio() 
    while data and reproduciendo==True:  
        stream.write(data)  
        data = f.readframes(CHUNK)  
 
    stream.stop_stream()  
    stream.close()  
 
    audio.terminate()
    time.after_cancel(proceso)
    print("FIN")
    bloqueo('normal')

def bloqueo(s):
    btnIniciar.config(state=s)
    btnDir.config(state=s)
    btnAbrir.config(state=s)
    
def parar():
    global grabando
    global reproduciendo
    #global contador,contador1,contador2
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

    print("GRABANDO")
    while grabando==True:
        data=stream.read(CHUNK)
        frames.append(data)
    print("fin")

    #DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
    count=0
    for i in os.listdir():
        new=(i).split(".")
        if "grabacion" in new[0] and new[1]=="wav":
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
time.pack()
ventana.geometry("488x97")
 
#frame=Frame(ventana)
btnIniciar=Button(ventana, fg='blue',width=16, text='Iniciar', command=iniciar)
btnIniciar.place(x=122,y=51)
btnParar=Button(ventana, fg='blue', width=16, text='Parar', command=parar)
btnParar.place(x=244,y=51)
btnDir=Button(ventana, text="Carpeta",width=16,command=direc)
btnDir.place(x=0,y=51)
btnAbrir=Button(ventana, text="Abrir",width=16,command=abrir)
btnAbrir.place(x=366,y=51)
etDir=Entry(ventana,width=90,textvariable=directorio_actual)
etDir.place(x=0,y=77)
#frame.pack()
 
ventana.mainloop()
