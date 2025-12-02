import tkinter as tk
from tkinter import messagebox
import random

class AhorcadoJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado - Python")
        self.root.geometry("600x500")
        
        
        self.palabras = ['PYTHON', 'PROGRAMACION', 'INTERFAZ', 'COMPUTADORA', 'ALGORITMO', 'TECLADO', 'MOUSE']
        
        
        self.palabra_secreta = ""
        self.letras_adivinadas = []
        self.intentos = 0
        self.max_intentos = 6
        
        
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack(pady=20)
        
       
        self.label_palabra = tk.Label(root, text="", font=("Helvetica", 24))
        self.label_palabra.pack(pady=10)
        
        
        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=20)
        
       
        self.btn_reset = tk.Button(root, text="Jugar de nuevo", command=self.iniciar_juego, bg="lightblue")
        self.btn_reset.pack(pady=10)
        
       
        self.iniciar_juego()

    def iniciar_juego(self):
        self.intentos = 0
        self.letras_adivinadas = []
        self.palabra_secreta = random.choice(self.palabras)
        
       
        self.canvas.delete("all")
        self.dibujar_horca()
        
      
        self.actualizar_palabra_mostrada()
        
        
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
            
        alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        fila = 0
        columna = 0
        for letra in alfabeto:
            btn = tk.Button(self.frame_botones, text=letra, width=4, font=("Arial", 10),
                            command=lambda l=letra: self.verificar_letra(l))
            btn.grid(row=fila, column=columna, padx=2, pady=2)
            columna += 1
            if columna > 8:
                columna = 0
                fila += 1

    def dibujar_horca(self):
        # Base y poste
        self.canvas.create_line(50, 250, 250, 250, width=3) 
        self.canvas.create_line(100, 250, 100, 50, width=3) 
        self.canvas.create_line(100, 50, 200, 50, width=3)  
        self.canvas.create_line(200, 50, 200, 80, width=3)  

    def dibujar_parte_monito(self):
        if self.intentos == 1: 
            self.canvas.create_oval(175, 80, 225, 130, width=2)
        elif self.intentos == 2:
            self.canvas.create_line(200, 130, 200, 200, width=2)
        elif self.intentos == 3: 
            self.canvas.create_line(200, 150, 170, 180, width=2)
        elif self.intentos == 4: 
            self.canvas.create_line(200, 150, 230, 180, width=2)
        elif self.intentos == 5: 
            self.canvas.create_line(200, 200, 170, 240, width=2)
        elif self.intentos == 6: 
            self.canvas.create_line(200, 200, 230, 240, width=2)
            
            self.canvas.create_line(185, 95, 195, 105, width=1)
            self.canvas.create_line(195, 95, 185, 105, width=1)
            self.canvas.create_line(205, 95, 215, 105, width=1)
            self.canvas.create_line(215, 95, 205, 105, width=1)

    def actualizar_palabra_mostrada(self):
        texto_mostrar = ""
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                texto_mostrar += letra + " "
            else:
                texto_mostrar += "_ "
        self.label_palabra.config(text=texto_mostrar)
        return "_" not in texto_mostrar

    def verificar_letra(self, letra):
       
        for widget in self.frame_botones.winfo_children():
            if widget['text'] == letra:
                widget.config(state="disabled")

        if letra in self.palabra_secreta:
            self.letras_adivinadas.append(letra)
            gano = self.actualizar_palabra_mostrada()
            if gano:
                messagebox.showinfo("¡Ganaste!", f"¡Felicidades! La palabra era {self.palabra_secreta}")
                self.iniciar_juego()
        else:
            self.intentos += 1
            self.dibujar_parte_monito()
            if self.intentos >= self.max_intentos:
                messagebox.showerror("¡Perdiste!", f"El monito ha muerto. La palabra era {self.palabra_secreta}")
                self.iniciar_juego()

if __name__ == "__main__":
    root = tk.Tk()
    juego = AhorcadoJuego(root)
    root.mainloop()