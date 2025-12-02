import turtle
import time
import random

# --- Configuración Inicial ---
retraso = 0.1
puntos = 0
alto_puntaje = 0

# Pantalla
ventana = turtle.Screen()
ventana.title("Viborita")
ventana.bgcolor("black")
ventana.setup(width=600, height=600)
ventana.tracer(0)

# Cabeza de la serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("white")
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direction = "stop"

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0, 100)

# Cuerpo de la serpiente (lista vacía)
cuerpo = []

# --- TEXTO (Marcador y Game Over) ---
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0, 260)
texto.write("Puntos: 0", align="center", font=("Courier", 24, "normal"))

# --- Funciones ---
def arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"
def abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"
def izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"
def derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"

def mover():
    if cabeza.direction == "up":
        cabeza.sety(cabeza.ycor() + 20)
    if cabeza.direction == "down":
        cabeza.sety(cabeza.ycor() - 20)
    if cabeza.direction == "left":
        cabeza.setx(cabeza.xcor() - 20)
    if cabeza.direction == "right":
        cabeza.setx(cabeza.xcor() + 20)

def game_over():
    global puntos
    # Mostrar mensaje
    texto.goto(0, 0)
    texto.write("GAME OVER", align="center", font=("Courier", 40, "bold"))
    ventana.update()
    time.sleep(2) # Esperar 2 segundos
    
    # Reiniciar juego
    cabeza.goto(0, 0)
    cabeza.direction = "stop"
    
    # Borrar cuerpo
    for segmento in cuerpo:
        segmento.goto(1000, 1000)
    cuerpo.clear()
    
    # Reiniciar puntos
    puntos = 0
    texto.clear()
    texto.goto(0, 260)
    texto.write("Puntos: {}".format(puntos), align="center", font=("Courier", 24, "normal"))

# --- Controles ---
ventana.listen()
ventana.onkeypress(arriba, "w")
ventana.onkeypress(abajo, "s")
ventana.onkeypress(izquierda, "a")
ventana.onkeypress(derecha, "d")

# --- Bucle del Juego ---
while True:
    ventana.update()

    # 1. Choque con bordes
    if cabeza.xcor() > 290 or cabeza.xcor() < -290 or cabeza.ycor() > 290 or cabeza.ycor() < -290:
        game_over()

    # 2. Choque con comida
    if cabeza.distance(comida) < 20:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)

        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("grey")
        nuevo_segmento.penup()
        cuerpo.append(nuevo_segmento)

        # Actualizar Puntos
        puntos += 10
        texto.clear()
        texto.write("Puntos: {}".format(puntos), align="center", font=("Courier", 24, "normal"))

    # Mover el cuerpo
    for index in range(len(cuerpo) - 1, 0, -1):
        x = cuerpo[index - 1].xcor()
        y = cuerpo[index - 1].ycor()
        cuerpo[index].goto(x, y)

    if len(cuerpo) > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        cuerpo[0].goto(x, y)

    mover()

    # 3. Choque con el propio cuerpo
    for segmento in cuerpo:
        if segmento.distance(cabeza) < 20:
            game_over()

    time.sleep(retraso)