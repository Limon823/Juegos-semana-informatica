import tkinter as tk
from tkinter import messagebox

preguntas = [
    {
        "pregunta": "¿Capital de Francia?",
        "opciones": ["Madrid", "París", "Roma", "Berlín"],
        "respuesta": "París"
    },
    {
        "pregunta": "¿8 x 7 = ?",
        "opciones": ["56", "49", "64", "54"],
        "respuesta": "4"
    },
        {
        "pregunta": "¿Cual es el territorio mas grande del mundo?",
        "opciones": ["Canada", "China", "Rusia", "Brasil"],
        "respuesta": "Rusia"
    },
    {
        "pregunta": "¿En que año llego el ser Humano a la Luna?",
        "opciones": ["1969", "1976", "1959", "1981"],
        "respuesta": "1969"
    },
    {
        "pregunta": "¿Cual es el oceano mas profundo del planeta?",
        "opciones": ["Atlantico", "Pacifico", "Indico", "Artico"],
        "respuesta": "Pacifico"
    },
    {
        "pregunta": "¿Que pais Gano el mundial de futbol en 2010?",
        "opciones": ["España", "Brasil", "Argentina", "Inglaterra"],
        "respuesta": "España"
    },
    {
        "pregunta": "¿Que cientifco propuso la teoria de la relatividad?",
        "opciones": ["Isaac Newton", "Albert Einstein", "Charles Darwin", "Nikola Tesla"],
        "respuesta": "Albert Einstein"
    },
    {
        "pregunta": "¿Cual es la moneda oficial de Reino Unido?",
        "opciones": ["Euro", "Dolar Britanico", "Rupia", "Libra Esterlina"],
        "respuesta": "Libra Esterlina"
    },
    {
        "pregunta": "¿En que continente se encuentra Egipto?",
        "opciones": ["Asiatico", "Europeo", "Africano", "Americano"],
        "respuesta": "Africanoo"
    },
]

index = 0
puntaje = 0

def cargar_pregunta():
    global index

    if index >= len(preguntas):
        finalizar()
        return

    pregunta = preguntas[index]
    lblPregunta.config(text=pregunta["pregunta"])

    for i, opcion in enumerate(pregunta["opciones"]):
        botones[i].config(text=opcion, bg=colores[i])

def responder(opcion_elegida):
    global index, puntaje

    correcta = preguntas[index]["respuesta"]

    if opcion_elegida == correcta:
        puntaje += 1

    index += 1
    cargar_pregunta()

def finalizar():
    messagebox.showinfo("Resultado", f"Juego terminado.\nTu puntaje: {puntaje}/{len(preguntas)}")
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Juego de Preguntas - Alexis")
ventana.geometry("600x400")
ventana.configure(bg="#6A0DAD") 

lblPregunta = tk.Label(
    ventana, 
    text="Pregunta aquí", 
    font=("Arial Black", 18), 
    fg="white",
    bg="#6A0DAD",
    wraplength=550
)
lblPregunta.pack(pady=30)

colores = ["#E91E63", "#2196F3", "#4CAF50", "#FF9800"] 

botones = []
for i in range(4):
    btn = tk.Button(
        ventana, 
        text="Opción", 
        font=("Arial", 14, "bold"), 
        width=20, 
        height=2,
        bg=colores[i],
        fg="white",
        activebackground=colores[i],
        command=lambda j=i: responder(botones[j].cget("text"))
    )
    btn.pack(pady=10)
    botones.append(btn)

cargar_pregunta()

ventana.mainloop()