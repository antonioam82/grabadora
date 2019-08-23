from tkinter import Tk,Label,Button,Frame,filedialog
 
def iniciar(contador=0):
    global proceso
 
    time['text'] = contador
 
    proceso=time.after(1000, iniciar, (contador+1))
 
def parar():
    global proceso
    time.after_cancel(proceso)

def direc():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
        directorio_actual.set(os.getcwd())
 
ventana = Tk()
ventana.title('Grabadora')

 
time = Label(ventana, fg='red', width=20, font=("","30"))
time.pack()
ventana.geometry("470x77")
 
frame=Frame(ventana)
btnIniciar=Button(frame, fg='blue',width=20, text='Iniciar', command=iniciar)
btnIniciar.grid(row=1, column=1)
btnParar=Button(frame, fg='blue', width=20, text='Parar', command=parar)
btnParar.grid(row=1, column=2)
btnDir=Button(frame, text="Directorio",width=20,command=direc)
btnDir.grid(row=1,column=0)
frame.pack()
 
ventana.mainloop()
