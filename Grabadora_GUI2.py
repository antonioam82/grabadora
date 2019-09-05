from tkinter import Tk,Label,Button,Frame,filedialog
import pyaudio
import os
import wave
import threading

grabando=False
audio=pyaudio.PyAudio()
CHUNK=1024
data=""
stream=""
f=""

def iniciar():
    global grabando
    global proceso
    global act_proceso
    bloqueo('disabled')
    #btnIniciar.config(state='disabled')
    #btnDir.config(state='disabled')
    #contador=0
    grabando=True
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    
    act_proceso=True
    archivo="grabacion.wav"
    #audio=pyaudio.PyAudio()
    t1=threading.Thread(target=grabacion, args=(FORMAT,CHANNELS,RATE,CHUNK,audio,archivo))
    t=threading.Thread(target=cuenta)
    t1.start()
    t.start()
    
def cuenta(contador=0):
    global proceso
    time['text'] = contador
    contador+1
    proceso=time.after(1000, cuenta, (contador+1))

def abrir():
    #chunk = 1024
    global data
    global stream
    global f
    audio=pyaudio.PyAudio()
    open_archive=filedialog.askopenfilename(initialdir = "/",
                 title = "Seleccione archivo",filetypes = (("wav files","*.wav"),
                 ("all files","*.*")))
    
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
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(CHUNK)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
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
    if grabando==True:
        grabando=False
        time.after_cancel(proceso)
        bloqueo('normal')
        #btnIniciar.config(state='normal')
        #btnDir.config(state='normal')

def direc():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)

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
        #name,ext=os.path.splitex(i)
        if "grabacion" in i:              #if len(name)==9 and "grabacion" in name and ext==".wav":
            count+=1
    if count>0:
        archivo="grabacion"+"("+str(count)+")"+".wav"
        
    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

ventana = Tk()
ventana.title('Grabadora')

time = Label(ventana, fg='green', width=20, text="0", bg="black", font=("","30"))
time.pack()
ventana.geometry("488x77")
 
frame=Frame(ventana)
btnIniciar=Button(frame, fg='blue',width=16, text='Iniciar', command=iniciar)
btnIniciar.grid(row=1, column=1)
btnParar=Button(frame, fg='blue', width=16, text='Parar', command=parar)
btnParar.grid(row=1, column=2)
btnDir=Button(frame, text="Directorio",width=16,command=direc)
btnDir.grid(row=1,column=0)
btnAbrir=Button(frame, text="Abrir",width=16,command=abrir)
btnAbrir.grid(row=1,column=3)
frame.pack()
 
ventana.mainloop()


