# RAFAEL GARCIA 
# 04/12/2025
import tkinter as tk
from tkinter import messagebox
import random

FILAS = 4
COLUMNAS = 4
NUM_PARES = (FILAS * COLUMNAS) // 2
CARTAS_BASE = [
    "🍎", "🍌", "🍇", "🍓",
    "🍋", "🥝", "🍉", "🍍"
]

xx = 0  
nom = ['green', 'red', 'orange'] 
puntos_j1 = 0
puntos_j2 = 0

if len(CARTAS_BASE) < NUM_PARES:
    raise ValueError(f"Necesitas al menos {NUM_PARES} símbolos en CARTAS_BASE.")

CARTAS = (CARTAS_BASE[:NUM_PARES] * 2)
random.shuffle(CARTAS)

botones = []
estado_juego = [False] * (FILAS * COLUMNAS)
indice_carta_previa = -1
volteando_par = False
pares_encontrados = 0

def actualizar_marcador():
    """Actualiza los textos de los puntos y marca de quién es el turno."""
    
    lbl_puntos_j1.config(text=str(puntos_j1))
    lbl_puntos_j2.config(text=str(puntos_j2))
    
    
    if xx == 0: 
        indicador_j1.config(bg="green", relief="sunken") 
        indicador_j2.config(bg="SystemButtonFace", relief="flat") 
    else:       
        indicador_j1.config(bg="SystemButtonFace", relief="flat") 
        indicador_j2.config(bg="red", relief="sunken") 
def iniciar_juego(frame_cartas):
    """Crea y posiciona todos los botones en el frame de la izquierda."""
    global botones
    botones = []
    for i in range(FILAS):
        for j in range(COLUMNAS):
            indice = i * COLUMNAS + j

            btn = tk.Button(
                frame_cartas,
                text="??",
                font=('Arial', 24, 'bold'),
                width=4,
                height=2,
                bg='SystemButtonFace', 
                command=lambda idx=indice: manejar_clic(idx)
            )
            btn.grid(row=i, column=j, padx=5, pady=5)
            botones.append(btn)

def voltear_cartas_no_emparejadas(idx1, idx2):
    """Voltea las cartas si no son pares y cambia de turno."""
    global indice_carta_previa, volteando_par, xx

    botones[idx1].config(bg='SystemButtonFace')
    botones[idx2].config(bg='SystemButtonFace')
    
    if not estado_juego[idx1]:
        botones[idx1].config(text="?", state=tk.NORMAL)
    if not estado_juego[idx2]:
        botones[idx2].config(text="?", state=tk.NORMAL)
        
    indice_carta_previa = -1
    volteando_par = False
    if xx == 0:
        xx = 1
    else:
        xx = 0
    
    actualizar_marcador() 

def manejar_clic(indice_actual):
    """Gestiona la lógica del clic, puntos y turnos."""
    global indice_carta_previa, volteando_par, pares_encontrados, xx, puntos_j1, puntos_j2

    if volteando_par or estado_juego[indice_actual] or indice_actual == indice_carta_previa:
        return

    botones[indice_actual].config(text=CARTAS[indice_actual], state=tk.DISABLED)
    
    if indice_carta_previa == -1:
       
        indice_carta_previa = indice_actual
    else:
        volteando_par = True 
        idx_prev = indice_carta_previa 
        
        if CARTAS[indice_actual] == CARTAS[idx_prev]:
            pares_encontrados += 1
            estado_juego[indice_actual] = True
            estado_juego[idx_prev] = True
            if xx == 0:
                puntos_j1 += 1
            else:
                puntos_j2 += 1
            
            actualizar_marcador() 

            botones[indice_actual].config(bg=nom[xx], disabledforeground='black') 
            botones[idx_prev].config(bg=nom[xx], disabledforeground='black')
            
            indice_carta_previa = -1
            volteando_par = False 

            if pares_encontrados == NUM_PARES:
                ganador = "Empate"
                if puntos_j1 > puntos_j2:
                    ganador = "Jugador 1"
                elif puntos_j2 > puntos_j1:
                    ganador = "Jugador 2"
                
                mensaje = f"¡Fin del juego!\nPuntos J1: {puntos_j1}\nPuntos J2: {puntos_j2}\nGanador: {ganador}"
                messagebox.showinfo("¡Eres un cacahuate SIIIIIIII!", mensaje)
                ventana_principal.destroy()

        else:
            botones[indice_actual].config(bg=nom[2]) 
            botones[idx_prev].config(bg=nom[2])      
            ventana_principal.after(1000, lambda: voltear_cartas_no_emparejadas(indice_actual, idx_prev))

ventana_principal = tk.Tk()
ventana_principal.title("MEMORAMA")

frame_tablero = tk.Frame(ventana_principal, padx=10, pady=10)
frame_tablero.pack(side=tk.LEFT) 

frame_marcador = tk.Frame(ventana_principal, padx=20, pady=10, relief="ridge", borderwidth=2)
frame_marcador.pack(side=tk.RIGHT, fill=tk.Y) 

tk.Label(frame_marcador, text="Puntos\nTotales de cada jugador", font=("Arial", 16, "bold")).pack(pady=10)

frame_j1 = tk.Frame(frame_marcador)
frame_j1.pack(pady=10, fill=tk.X)

indicador_j1 = tk.Label(frame_j1, width=2, height=1, borderwidth=1)
indicador_j1.pack(side=tk.LEFT, padx=5)

tk.Label(frame_j1, text="Jugador 1", font=("Arial", 12)).pack(side=tk.LEFT)
lbl_puntos_j1 = tk.Label(frame_j1, text="0", font=("Arial", 14, "bold"), bg="white", width=5, relief="sunken")
lbl_puntos_j1.pack(side=tk.RIGHT, padx=5)

frame_j2 = tk.Frame(frame_marcador)
frame_j2.pack(pady=10, fill=tk.X)

indicador_j2 = tk.Label(frame_j2, width=2, height=1, borderwidth=1)
indicador_j2.pack(side=tk.LEFT, padx=5)

tk.Label(frame_j2, text="Jugador 2", font=("Arial", 12)).pack(side=tk.LEFT)
lbl_puntos_j2 = tk.Label(frame_j2, text="0", font=("Arial", 14, "bold"), bg="white", width=5, relief="sunken")
lbl_puntos_j2.pack(side=tk.RIGHT, padx=5)

iniciar_juego(frame_tablero) 
actualizar_marcador() 

ventana_principal.mainloop()