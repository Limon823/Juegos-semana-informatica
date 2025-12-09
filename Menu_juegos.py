import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
JUEGOS = {
    1: {
        "nombre": "Juego de Bryan (Viborita)",
        "hash": "b0ea520b8565adf626bb6cab987aa82ba7103748",
        "archivo": "viborita.py", 
    },
    2: {
        "nombre": "Juego de Alex (Preguntas)",
        "hash": "f2c6c639bd32244e8ce8a9a36f7c633913e48244",
        "archivo": "proyecto SI.py",
    },
    3: {
        "nombre": "Juego de Gad (Reloj)",
        "hash": "43e6050f56b9dc21add019fab99d2b68327c0428", 
        "archivo": "reloj.py", 
    },
    4: {
        "nombre": "Juego de Erick (Ahorcado)",
        "hash": "752c424a7b7bd503b175b9e741e0aeb82d7e15ea",
        "archivo": "holamundo.py",
    },
    5: {
        "nombre": "Juego de Rafa (Memorama)",
        "hash": "b89bb2686dbea39ee90285262cb73c0da0247baf", 
        "archivo": "MEMORAMA1.py", 
    },
    6: {
        "nombre": "Juego de Zury(Sudoku)",
        "hash": "c88aebbc30f9ecb4721c8b4b314de9a55336fb31", 
        "archivo": "Sudoku.py", 
    },
    7: {
        "nombre": "Juego de Vale (Piedra, Papel o Tijeras)",
        "hash": "6093832d4605fcf21676248deb0404a5ff786cf3",
        "archivo": "xoxo.py", 
    },
    8: {
        "nombre": "Juego de Limon (Sopa de Letras)",
        "hash": "eb2eda3708cdfd4367ebef956e6dea9a0574b4ae",
        "archivo": "sopa.py", 
    },
} 

def ejecutar_juego_desde_commit(juego_info):
    hash_commit = juego_info["hash"]
    nombre_archivo = juego_info["archivo"]
    temp_dir = "temp_juegos_git"
    ruta_temporal = os.path.join(temp_dir, nombre_archivo)
    
    os.makedirs(temp_dir, exist_ok=True)
    comando_git = f'git show "{hash_commit}:{nombre_archivo}"'
    root.iconify() 
    proceso = subprocess.run(comando_git, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
    contenido_py = proceso.stdout
    
    if not contenido_py.strip(): 
        messagebox.showerror("Error de Archivo", "El archivo está vacío o el hash/ruta es incorrecto.")
        root.deiconify()
        return

    with open(ruta_temporal, "w", encoding="utf-8") as f: 
        f.write(contenido_py)
        
    subprocess.run([sys.executable, ruta_temporal])
    
    root.deiconify() 
    if os.path.exists(ruta_temporal): os.remove(ruta_temporal)
    if os.path.exists(temp_dir) and not os.listdir(temp_dir): os.rmdir(temp_dir)

root = tk.Tk()
root.title("Panel de Juegos del Repositorio")
root.geometry("700x700") 
root.resizable(False, False) 

COLOR_FONDO = "#ECEFF1"
COLOR_BOTON_NORMAL = "#0277BD"
COLOR_BOTON_ACTIVO = "#01579B"

root.configure(bg=COLOR_FONDO)

titulo = tk.Label(root, text="Selecciona un Juego para Ejecutar:", font=("Segoe UI", 20, "bold"), pady=20, bg=COLOR_FONDO, fg="#37474F")
titulo.pack()

frame_botones = tk.Frame(root, bg=COLOR_FONDO)
frame_botones.pack(pady=10)

for clave, info in JUEGOS.items():
    accion_boton = lambda info_juego=info: ejecutar_juego_desde_commit(info_juego)
    boton = tk.Button(frame_botones, text=f"{clave}. {info['nombre']}", command=accion_boton, width=40, height=2, bg=COLOR_BOTON_NORMAL, fg="white", font=("Segoe UI", 12, "bold"), activebackground=COLOR_BOTON_ACTIVO, relief=tk.FLAT)
    boton.pack(pady=7, padx=10)

boton_salir = tk.Button(root, text="SALIR DEL PANEL", command=root.quit, width=40, height=2, bg="#D32F2F", fg="white", font=("Segoe UI", 12, "bold"), activebackground="#B71C1C", relief=tk.FLAT)
boton_salir.pack(pady=30)

root.mainloop()