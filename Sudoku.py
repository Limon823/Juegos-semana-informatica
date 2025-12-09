#!/usr/bin/env python3
# sudoku_gui.py
# Juego de Sudoku con interfaz gráfica en Tkinter
# Autor: (adaptado para usuario)
# Idioma: Español

import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy

# -----------------------------
# Generador de tablero (backtracking)
# -----------------------------
def es_valido(tablero, fila, col, num):
    # Comprueba fila
    for c in range(9):
        if tablero[fila][c] == num:
            return False
    # Comprueba columna
    for r in range(9):
        if tablero[r][col] == num:
            return False
    # Comprueba subcuadro 3x3
    start_row = (fila // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if tablero[r][c] == num:
                return False
    return True

def generar_tablero_resuelto():
    tablero = [[0]*9 for _ in range(9)]
    numeros = list(range(1, 10))

    def backtrack(pos=0):
        if pos == 81:
            return True
        fila = pos // 9
        col = pos % 9
        if tablero[fila][col] != 0:
            return backtrack(pos + 1)
        random.shuffle(numeros)
        for n in numeros:
            if es_valido(tablero, fila, col, n):
                tablero[fila][col] = n
                if backtrack(pos + 1):
                    return True
                tablero[fila][col] = 0
        return False

    backtrack()
    return tablero

# -----------------------------
# Crear puzzle (eliminar celdas)
# -----------------------------
def eliminar_celdas(tablero_resuelto, cantidad_eliminar):
    tablero = copy.deepcopy(tablero_resuelto)
    posiciones = list(range(81))
    random.shuffle(posiciones)
    eliminadas = 0
    for pos in posiciones:
        if eliminadas >= cantidad_eliminar:
            break
        r = pos // 9
        c = pos % 9
        if tablero[r][c] != 0:
            tablero[r][c] = 0
            eliminadas += 1
    return tablero

# -----------------------------
# Verificar solución
# -----------------------------
def tablero_completo(tablero):
    for r in range(9):
        for c in range(9):
            if tablero[r][c] == 0:
                return False
    return True

def es_solucion_valida(tablero):
    # comprueba todas las filas, columnas y subcuadros contienen 1..9 exactamente una vez
    for r in range(9):
        if sorted(tablero[r]) != list(range(1,10)):
            return False
    for c in range(9):
        col = [tablero[r][c] for r in range(9)]
        if sorted(col) != list(range(1,10)):
            return False
    for br in range(0,9,3):
        for bc in range(0,9,3):
            block = [tablero[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
            if sorted(block) != list(range(1,10)):
                return False
    return True

# -----------------------------
# Interfaz gráfica (Tkinter)
# -----------------------------
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        root.title("Sudoku - Juego")
        root.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Variables
        self.dificultad = tk.StringVar(value="Medio")
        self.tablero_resuelto = None
        self.tablero_puzzle = None
        self.entries = [[None]*9 for _ in range(9)]
        self.fijas = [[False]*9 for _ in range(9)]

        # Crear frames
        self.frame_inicio = ttk.Frame(root, padding=12)
        self.frame_juego = ttk.Frame(root, padding=8)

        self._construir_inicio()
        self._construir_juego()

        self.frame_inicio.grid(row=0, column=0)
        self.frame_juego.grid_forget()

    # Pantalla de inicio
    def _construir_inicio(self):
        lbl = ttk.Label(self.frame_inicio, text="Sudoku", font=("Helvetica", 24))
        lbl.grid(row=0, column=0, columnspan=2, pady=(0,10))

        # Dificultad
        group = ttk.LabelFrame(self.frame_inicio, text="Dificultad")
        group.grid(row=1, column=0, columnspan=2, pady=(0,10), sticky="ew")
        ttk.Radiobutton(group, text="Fácil", variable=self.dificultad, value="Fácil").grid(row=0, column=0, padx=6, pady=4)
        ttk.Radiobutton(group, text="Medio", variable=self.dificultad, value="Medio").grid(row=0, column=1, padx=6, pady=4)
        ttk.Radiobutton(group, text="Difícil", variable=self.dificultad, value="Difícil").grid(row=0, column=2, padx=6, pady=4)

        # Botones Jugar / Salir
        boton_jugar = ttk.Button(self.frame_inicio, text="Jugar", command=self.iniciar_juego, width=20)
        boton_jugar.grid(row=2, column=0, pady=(10,0), padx=6)
        boton_salir = ttk.Button(self.frame_inicio, text="Salir", command=self.root.destroy, width=20)
        boton_salir.grid(row=2, column=1, pady=(10,0), padx=6)

        # Nota
        nota = ttk.Label(self.frame_inicio, text="Selecciona dificultad y presiona Jugar.", font=("Helvetica", 9))
        nota.grid(row=3, column=0, columnspan=2, pady=(8,0))

    # Construcción del tablero y controles
    def _construir_juego(self):
        # Arriba: controles
        controles = ttk.Frame(self.frame_juego)
        controles.grid(row=0, column=0, columnspan=9, sticky="ew", pady=(0,6))
        ttk.Button(controles, text="Verificar", command=self.verificar_tablero).grid(row=0, column=0, padx=4)
        ttk.Button(controles, text="Reiniciar", command=self.reiniciar).grid(row=0, column=1, padx=4)
        ttk.Button(controles, text="Mostrar solución", command=self.mostrar_solucion).grid(row=0, column=2, padx=4)
        ttk.Button(controles, text="Nuevo", command=self.nuevo).grid(row=0, column=3, padx=4)
        ttk.Button(controles, text="Salir al inicio", command=self.volver_inicio).grid(row=0, column=4, padx=4)

        # Tablero
        tablero_frame = ttk.Frame(self.frame_juego)
        tablero_frame.grid(row=1, column=0, columnspan=9)
        font = ("Helvetica", 14)

        for r in range(9):
            for c in range(9):
                e = tk.Entry(tablero_frame, width=2, font=font, justify="center")
                e.grid(row=r, column=c, padx=(0 if c%3!=2 else 6), pady=(0 if r%3!=2 else 6))
                # limitar entrada a un dígito
                vcmd = (self.root.register(self._validar_entrada), '%P', '%d')
                e.config(validate='key', validatecommand=vcmd)
                self.entries[r][c] = e

        # Pie: mensaje
        self.lbl_mensaje = ttk.Label(self.frame_juego, text="", font=("Helvetica", 10))
        self.lbl_mensaje.grid(row=2, column=0, columnspan=9, pady=(8,0))

    def _validar_entrada(self, texto, tipo):
        # tipo '1' inserción, '0' borrado
        if texto == "":
            return True
        if len(texto) > 1:
            return False
        return texto.isdigit() and 1 <= int(texto) <= 9

    # Genera y muestra puzzle según dificultad
    def iniciar_juego(self):
        dificultad = self.dificultad.get()
        if dificultad == "Fácil":
            eliminar = 35  # menos casillas eliminadas => más fácil
        elif dificultad == "Medio":
            eliminar = 45
        else:  # Difícil
            eliminar = 55

        # Generar solución y puzzle
        self.tablero_resuelto = generar_tablero_resuelto()
        self.tablero_puzzle = eliminar_celdas(self.tablero_resuelto, eliminar)
        self._cargar_tablero_en_gui()
        # cambiar vista
        self.frame_inicio.grid_forget()
        self.frame_juego.grid()

    def _cargar_tablero_en_gui(self):
        # Llenar entries y marcar fijas
        for r in range(9):
            for c in range(9):
                val = self.tablero_puzzle[r][c]
                e = self.entries[r][c]
                e.config(state='normal')
                e.delete(0, tk.END)
                e.config(fg='black', disabledforeground='black')
                e.config(bg='white')
                if val != 0:
                    e.insert(0, str(val))
                    e.config(state='disabled')  # celda fija
                    self.fijas[r][c] = True
                else:
                    self.fijas[r][c] = False
        self.lbl_mensaje.config(text=f"Dificultad: {self.dificultad.get()} — ¡Buena suerte!")

    def volver_inicio(self):
        self.frame_juego.grid_forget()
        self.frame_inicio.grid()

    def verificar_tablero(self):
        # construir tablero actual desde entries
        tablero_actual = [[0]*9 for _ in range(9)]
        errores = []
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                txt = e.get().strip()
                if txt == "":
                    tablero_actual[r][c] = 0
                else:
                    try:
                        num = int(txt)
                        tablero_actual[r][c] = num
                    except:
                        tablero_actual[r][c] = 0

        # resalta errores simples: repetidos por fila/col/box o faltantes
        conflictos = [[False]*9 for _ in range(9)]

        # check filas
        for r in range(9):
            seen = {}
            for c in range(9):
                v = tablero_actual[r][c]
                if v == 0: continue
                if v in seen:
                    conflictos[r][c] = True
                    conflictos[r][seen[v]] = True
                else:
                    seen[v] = c
        # check columnas
        for c in range(9):
            seen = {}
            for r in range(9):
                v = tablero_actual[r][c]
                if v == 0: continue
                if v in seen:
                    conflictos[r][c] = True
                    conflictos[seen[v]][c] = True
                else:
                    seen[v] = r
        # check subcuadros
        for br in range(0,9,3):
            for bc in range(0,9,3):
                seen = {}
                for r in range(br, br+3):
                    for c in range(bc, bc+3):
                        v = tablero_actual[r][c]
                        if v == 0: continue
                        key = v
                        if key in seen:
                            (rr,cc) = seen[key]
                            conflictos[r][c] = True
                            conflictos[rr][cc] = True
                        else:
                            seen[key] = (r,c)

        # aplicar colores
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                if conflictos[r][c]:
                    e.config(bg="#f8d7da")  # rojo claro
                else:
                    e.config(bg="white")

        if any(any(row) for row in conflictos):
            self.lbl_mensaje.config(text="Hay conflictos resaltados en rojo. Corrige y vuelve a intentar.")
            return

        if not tablero_completo(tablero_actual):
            self.lbl_mensaje.config(text="Aún faltan casillas por completar.")
            return

        # comprobar validez global
        if es_solucion_valida(tablero_actual):
            self.lbl_mensaje.config(text="¡Felicidades! Has resuelto el Sudoku.")
            messagebox.showinfo("Sudoku", "¡Correcto! Has resuelto el Sudoku.")
        else:
            self.lbl_mensaje.config(text="La solución no es válida. Revisa las casillas.")
            messagebox.showwarning("Sudoku", "La solución no es válida. Revisa las casillas.")

    def reiniciar(self):
        # borrar solo las entradas no fijas
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                if not self.fijas[r][c]:
                    e.config(state='normal')
                    e.delete(0, tk.END)
                    e.config(bg='white')
        self.lbl_mensaje.config(text="Tablero reiniciado (las celdas fijas permanecen).")

    def mostrar_solucion(self):
        if self.tablero_resuelto is None:
            return
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                e.config(state='normal')
                e.delete(0, tk.END)
                e.insert(0, str(self.tablero_resuelto[r][c]))
                e.config(state='disabled')
                e.config(bg='lightgreen')
        self.lbl_mensaje.config(text="Solución mostrada. Presiona Nuevo para otro puzzle.")

    def nuevo(self):
        # genera uno nuevo con la misma dificultad seleccionada
        self.iniciar_juego()

# -----------------------------
# Ejecutar aplicación
# -----------------------------
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
