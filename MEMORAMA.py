import tkinter as tk
from tkinter import messagebox
import random
import time
FILAS = 4
COLUMNAS = 4
NUM_PARES = (FILAS * COLUMNAS) // 2
CARTAS_BASE = [
    "🍎", "🍌", "🍇", "🍓",
    "🍋", "🥝", "🍉", "🍍"
]

if len(CARTAS_BASE) < NUM_PARES:
    raise ValueError(f"Necesitas al menos {NUM_PARES} símbolos en CARTAS_BASE.")
CARTAS = (CARTAS_BASE[:NUM_PARES] * 2)
random.shuffle(CARTAS)

botones = []              
estado_juego = [False] * (FILAS * COLUMNAS) 
indice_carta_previa = -1  
volteando_par = False     
pares_encontrados = 0     

def iniciar_juego(ventana):
    """Crea y posiciona todos los botones en la ventana."""
    global botones
    botones = []
    for i in range(FILAS):
        for j in range(COLUMNAS):
            indice = i * COLUMNAS + j
            
            btn = tk.Button(
                ventana,
                text="?",
                font=('Arial', 24, 'bold'),
                width=4,
                height=2,
                command=lambda idx=indice: manejar_clic(idx) 
            )
            
            
            btn.grid(row=i, column=j, padx=5, pady=5)
            
            botones.append(btn)

def manejar_clic(indice_actual):
    """
    Gestiona la lógica cuando se hace clic en un botón.
    """
    global indice_carta_previa, volteando_par, pares_encontrados
    
    
    if volteando_par or estado_juego[indice_actual] or indice_actual == indice_carta_previa:
        return
      
    botones[indice_actual].config(text=CARTAS[indice_actual], state=tk.DISABLED)
    if indice_carta_previa == -1:
        indice_carta_previa = indice_actual
        
    else:
        volteando_par = True 
        
        if CARTAS[indice_actual] == CARTAS[indice_carta_previa]:
            
            pares_encontrados += 1
            
            
            estado_juego[indice_actual] = True
            estado_juego[indice_carta_previa] = True
            
            botones[indice_actual].config(bg='lightgreen')
            botones[indice_carta_previa].config(bg='lightgreen')
            
            
            indice_carta_previa = -1
            volteando_par = False 
            
           
            if pares_encontrados == NUM_PARES:
                messagebox.showinfo("¡Memorama!", "🎉 ¡Felicidades! ¡Has encontrado todos los pares! 🎉")
                ventana_principal.destroy()
            
        else:
            ventana_principal.after(1000, lambda: voltear_cartas_no_emparejadas(indice_actual, indice_carta_previa))
            
            
def voltear_cartas_no_emparejadas(idx1, idx2):
    """Voltea las dos cartas a su estado original (oculto) después de un fallo."""
    global indice_carta_previa, volteando_par
    
    botones[idx1].config(text="?", state=tk.NORMAL)
    
    botones[idx2].config(text="?", state=tk.NORMAL)
    

    indice_carta_previa = -1
    volteando_par = False 

ventana_principal = tk.Tk()
ventana_principal.title("MEMORAMA")

iniciar_juego(ventana_principal)

ventana_principal.mainloop()