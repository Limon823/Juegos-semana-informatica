#Juego: Viborita
#Autor: Bryan Flores

from tkinter import Tk, Canvas, Frame, Button, Label, IntVar, ALL
import random

x,y = 75, 75
direccion = ""
posicion_x = 15
posicion_y = 15
posicion_food = (105,105)
posicion_Vibora = [(75,75)]
nueva_posicion = [(75, 75)]

def dibujar_fondo():
    for i in range(0,460,30):
        for j in range(0,460,30):
            Canvas.create_rectangle(i, j, i+30, j+30, fill="gray10")

def coordenadas_vibora():
    global direccion, posicion_Vibora,x,y ,nueva_posicion

    if direccion == "arriba":
        y = y-30
        nueva_posicion[0] = (x,y)
        if y >=465:
            y=15
        elif y <=0:
            y=465
    elif direccion == "abajo":
        y = y+30
        nueva_posicion[0] = (x,y)
        if y >=465:
            y=15
        elif y <=0:
            y=15
    elif direccion == "izquierda":
        x = x-30
        nueva_posicion[0] = (x,y)
        if x >=465:
            x=15
        elif x <=0:
            x=465
    elif direccion == "derecha":
        x = x+30
        nueva_posicion[0] = (x,y)
        if x >=465:
            x=15
        elif x <=0:
            x=15

    posicion_Vibora = nueva_posicion + posicion_Vibora[:-1]

    for parte, lugar in zip(Canvas.find_withtag("vibora"), posicion_Vibora):
        Canvas.coords(parte, lugar)

def direccion_vibora(event):
    global direccion
    
    if event == "izquierda":
        direccion = event
    elif event == "derecha":
        direccion = event
    elif event == "arriba":
        direccion = event
    elif event == "abajo":
        direccion = event

def movimiento_vibora():
    global posicion_food, posicion_Vibora, nueva_posicion
    posiciones =[15,45,75,105,135,165,195,225,255,285,315,345,375,405,435,465]

    coordenadas_vibora()

    if posicion_food == posicion_Vibora[0]:
        n = len(posicion_Vibora)

        cantidad["text"] = "cantidad 🍎: {} ".format(n)

        posicion_food = (random.choice(posiciones), random.choice(posiciones))
        posicion_Vibora.append(posicion_Vibora[-1])

        if posicion_food not in posicion_Vibora:
            Canvas.coords(Canvas.find_withtag("food"), posicion_food)
        
        Canvas.create_text(*posicion_Vibora[-1],text="■",fill="green2", font=("Arial", 20),tag="vibora")
    
    if posicion_Vibora[0] in posicion_Vibora[1:] and len(posicion_Vibora) > 2:
        cruzar_vibora()
        return

    for i in posicion_Vibora:
        if len(posicion_Vibora)==257:
            maximo_nivel()

    cantidad.after(300, movimiento_vibora)

def cruzar_vibora():
    Canvas.delete(ALL)
    Canvas.create_text(Canvas.winfo_width()/2, Canvas.winfo_height()/2, text="Intentalo\n de Nuevo \n\n🍎", fill="red", font=("Arial", 20,"bold"))

def maximo_nivel():
    Canvas.delete(ALL)
    Canvas.create_text(Canvas.winfo_width()/2, Canvas.winfo_height()/2, text="🎉\n\n\n 🎉\n\n\n 🎉\n\n\n 🎉", fill="green", font=("Arial", 35,"bold"))

def iniciar_nuevo_juego():
    global x, y, direccion, posicion_Vibora, nueva_posicion, posicion_food
    x, y = 75, 75
    direccion = "" 
    posicion_Vibora = [(75,75)]
    nueva_posicion = [(75, 75)]
    posicion_food = (105, 105)
    
    Canvas.delete(ALL)
    cantidad["text"] = "cantidad 🍎: 0"
    
    #se Dibuja todo de nuevo
    dibujar_fondo()
    Canvas.create_text(*posicion_food, text="🍎", fill="red", font=("Arial", 18), tag="food")
    Canvas.create_text(75, 75, text="■", fill="white", font=("Arial", 20), tag="vibora")
    
    movimiento_vibora()

def salir():
    ventana.destroy()
    ventana.quit()

ventana = Tk()
ventana.config(bg="black")
ventana.title("Viborita")
ventana.geometry("485x510")
ventana.resizable(0, 0)

frame_1 = Frame(ventana, width= 485, height=25, bg="black")
frame_1.grid(column=0, row=0)
frame_2 = Frame(ventana, width= 485, height=490, bg="black")
frame_2.grid(column=0, row=1)

ventana.bind("<w>", lambda event: direccion_vibora("arriba"))
ventana.bind("<s>", lambda event: direccion_vibora("abajo"))
ventana.bind("<a>", lambda event: direccion_vibora("izquierda"))
ventana.bind("<d>", lambda event: direccion_vibora("derecha"))

Canvas = Canvas(frame_2, width=479, height=479, bg="black")
Canvas.pack()

dibujar_fondo() 

# Creamos la comida inicial
Canvas.create_text(105,105, text="🍎", fill="red", font=("Arial", 18), tag = "food") # Ojo: puse 105,105

Button1 = Button(frame_1, text="Salir", command=salir, bg="red", fg="white")
Button1.grid(column=0, row=0, padx=20)

# CAMBIO IMPORTANTE AQUÍ: command=iniciar_nuevo_juego
Button2 = Button(frame_1, text="Iniciar", command=iniciar_nuevo_juego, bg="green", fg="white")
Button2.grid(column=1, row=0, padx=20)

cantidad = Label(frame_1, text="cantidad 🍎: 0", bg="black", fg="white", font=("Arial", 20,"bold"))
cantidad.grid(column=2, row=0, padx=20)

ventana.mainloop()