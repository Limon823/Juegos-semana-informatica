import tkinter as interfaz

ventana = interfaz.Tk()
ventana.geometry("900x500")
ventana.title("limon huele a caca")

lblMensaje = interfaz.Label(ventana, text="charbel", font=("Arial", 15))
lblMensaje.pack(side = "top")
lblMensaje2 = interfaz.Label(ventana, text="1 2 3 4 5 6 7 8 9 ", font=("Arial", 50))
lblMensaje2.place(x=200, y=250)
tam=18

def otrocambio():
    lblMensaje2.config(text=dark.get())

def cambio():
    lblMensaje.config(font=("comic sans ms", tam))


botonn = interfaz.Button(ventana, text="erick", command = cambio)
botonn.pack(side = "top")

def cambio():
    lblMensaje.config(text="hala madrid")
botonn = interfaz.Button(ventana, text="erick", command = cambio)
botonn.pack(side = "top")

def cambio():
    lblMensaje.config(fg="blue")
botonn = interfaz.Button(ventana, text="erick", command = cambio)
botonn.pack(side = "top")

def cambiodark():
    lblMensaje2.config(text=dark.get())
dark = interfaz.Entry(ventana, show="XD")
dark.pack(side = "left")

botonazo = interfaz.Button(ventana, text="boton", command = otrocambio,font=("Arial",23))
botonazo.place(x=20,y=150)


imagen_tk = interfaz.PhotoImage(file="pain.png")


lblimagen = interfaz.Label(ventana, image=imagen_tk)
lblimagen.place(x=100,y=100)


lblimagen.image = imagen_tk 



ventana.mainloop()