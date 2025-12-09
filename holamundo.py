import tkinter as tk
from tkinter import messagebox
import random

class AhorcadoJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado Multiverso - Python")
        self.root.geometry("600x600") 
        
        self.palabras = ['PYTHON', 'PROGRAMACION', 'INTERFAZ', 'COMPUTADORA', 'ALGORITMO', 'TECLADO', 'MOUSE', 'GALLITO', 'JAVA', 'CHATGPT']
        
        self.tipos_muerte = ['ahorcado', 'guillotina', 'hoguera', 'ahogado']
        self.tipo_muerte_actual = "" 
        
        self.palabra_secreta = ""
        self.letras_adivinadas = []
        self.intentos = 0
        self.max_intentos = 6
        
        self.canvas = tk.Canvas(root, width=350, height=350, bg="white")
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
        
        
        opciones_disponibles = self.tipos_muerte.copy()
        
        
        if self.tipo_muerte_actual in opciones_disponibles:
            opciones_disponibles.remove(self.tipo_muerte_actual)
        
        
        self.tipo_muerte_actual = random.choice(opciones_disponibles)
        

        print(f"Modo de juego: {self.tipo_muerte_actual}") 
        
        self.canvas.delete("all")
       
        self.dibujar_escenario()
        
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

    def dibujar_escenario(self):
        """Dibuja la base según el tipo de muerte elegido"""
        if self.tipo_muerte_actual == 'ahorcado':
            self.canvas.create_line(50, 300, 250, 300, width=3)
            self.canvas.create_line(100, 300, 100, 50, width=3) 
            self.canvas.create_line(100, 50, 200, 50, width=3)  
            self.canvas.create_line(200, 50, 200, 80, width=3)  
            
        elif self.tipo_muerte_actual == 'guillotina':
            self.canvas.create_rectangle(50, 300, 300, 320, fill="brown") 
            self.canvas.create_line(120, 300, 120, 50, width=4, fill="brown") 
            self.canvas.create_line(230, 300, 230, 50, width=4, fill="brown")  
            self.canvas.create_line(120, 50, 230, 50, width=4, fill="brown") 
            
            self.hoja_guillotina = self.canvas.create_polygon(130, 60, 220, 60, 220, 100, 175, 130, 130, 100, fill="silver", outline="black", tags="hoja")
           
            self.canvas.create_rectangle(150, 250, 200, 280, fill="brown", outline="black")
            self.canvas.create_oval(165, 240, 185, 260, fill="white") 

        elif self.tipo_muerte_actual == 'hoguera':
            self.canvas.create_line(175, 320, 175, 100, width=4, fill="brown")
            for i in range(5):
                self.canvas.create_line(100 + (i*15), 320, 250 - (i*15), 320 - (i*5), width=5, fill="brown")
                self.canvas.create_line(100 + (i*15), 310, 250 - (i*15), 310 + (i*5), width=5, fill="#8B4513")

        elif self.tipo_muerte_actual == 'ahogado':
            self.canvas.create_rectangle(100, 100, 250, 320, width=3, outline="blue")
            self.canvas.create_line(80, 320, 270, 320, width=3)

    def dibujar_progreso(self):
        """Decide qué función de progreso llamar"""
        if self.tipo_muerte_actual == 'ahorcado':
            self.dibujar_progreso_ahorcado()
        elif self.tipo_muerte_actual == 'guillotina':
            self.dibujar_progreso_guillotina()
        elif self.tipo_muerte_actual == 'hoguera':
            self.dibujar_progreso_hoguera()
        elif self.tipo_muerte_actual == 'ahogado':
            self.dibujar_progreso_ahogado()

    def dibujar_progreso_ahorcado(self):
        if self.intentos == 1: 
            self.canvas.create_oval(175, 80, 225, 130, width=2)
        elif self.intentos == 2: 
            self.canvas.create_line(200, 130, 200, 200, width=2)
        elif self.intentos == 3: 
            self.canvas.create_line(200, 150, 170, 180, width=2)
        elif self.intentos == 4: 
            self.canvas.create_line(200, 150, 230, 180, width=2)
        elif self.intentos == 5: 
            self.canvas.create_line(200, 200, 170, 250, width=2)
        elif self.intentos == 6: 
            self.canvas.create_line(200, 200, 230, 250, width=2)
            self.dibujar_ojos_muertos(185, 95)

    def dibujar_progreso_guillotina(self):
        if self.intentos == 1: 
            self.canvas.create_line(150, 280, 130, 280, width=2) 
            self.canvas.create_line(130, 280, 140, 230, width=2) 
            self.canvas.create_line(140, 230, 175, 250, width=2) 
        elif self.intentos == 2: 
            self.cabeza_guillo = self.canvas.create_oval(160, 230, 190, 260, width=2, fill="white", tags="cabeza_viva")
        elif self.intentos == 3: 
             self.canvas.create_line(150, 235, 130, 245, width=2)
             self.canvas.create_line(130, 245, 140, 255, width=2)
        elif self.intentos == 4: 
             self.canvas.create_line(175, 60, 175, 10, width=1, dash=(4,2))
        elif self.intentos == 5:    
             self.canvas.create_oval(168, 240, 173, 245, fill="black") 
             self.canvas.create_oval(178, 240, 183, 245, fill="black") 
             self.canvas.create_oval(172, 250, 178, 255, width=1) 
        elif self.intentos == 6: 
            self.canvas.delete("hoja") 
            self.canvas.delete("cabeza_viva") 
            self.canvas.create_polygon(130, 240, 220, 240, 220, 280, 175, 310, 130, 280, fill="silver", outline="black")
            self.canvas.create_oval(160, 310, 190, 340, width=2, fill="white")
            self.dibujar_ojos_muertos(170, 320)
            self.canvas.create_oval(165, 250, 185, 270, fill="red", outline="red")

    def dibujar_progreso_hoguera(self):
        if self.intentos == 1: 
            self.canvas.create_oval(160, 120, 190, 160, width=2, fill="white") 
            self.canvas.create_line(175, 160, 175, 250, width=2) 
            self.canvas.create_line(160, 180, 190, 180, width=3, fill="brown") 
        elif self.intentos == 2: 
            self.canvas.create_line(175, 170, 150, 200, width=2)
            self.canvas.create_line(175, 170, 200, 200, width=2)
            self.canvas.create_line(175, 250, 160, 300, width=2)
            self.canvas.create_line(175, 250, 190, 300, width=2)
        elif self.intentos == 3: 
             self.canvas.create_polygon(120, 320, 140, 280, 160, 310, 180, 270, 200, 315, 230, 320, fill="yellow", outline="orange")
        elif self.intentos == 4: 
             self.canvas.create_polygon(110, 320, 135, 250, 165, 290, 185, 240, 210, 300, 240, 320, fill="orange", outline="red", stipple="gray50")
        elif self.intentos == 5: 
             self.canvas.create_polygon(100, 320, 130, 200, 175, 260, 220, 190, 250, 320, fill="red", outline="yellow", stipple="gray25")
        elif self.intentos == 6: 
             self.canvas.create_polygon(90, 320, 120, 150, 175, 100, 230, 160, 260, 320, fill="#8B0000", outline="orange")
             self.dibujar_ojos_muertos(170, 130)

    def dibujar_progreso_ahogado(self):
        if self.intentos == 1: 
            self.canvas.create_oval(160, 250, 190, 280, width=2, fill="white") 
            self.canvas.create_line(175, 280, 175, 310, width=2) 
            self.canvas.create_line(175, 290, 155, 270, width=2) 
            self.canvas.create_line(175, 290, 195, 270, width=2)
        
        alto_agua = 0
        if self.intentos == 2: alto_agua = 300
        elif self.intentos == 3: alto_agua = 280
        elif self.intentos == 4: alto_agua = 250
        elif self.intentos == 5: alto_agua = 220
        elif self.intentos == 6: alto_agua = 180
        
        if self.intentos >= 2:
            self.canvas.create_rectangle(101, alto_agua, 249, 319, fill="blue", outline="", stipple="gray50")
            
        if self.intentos == 6:
            self.canvas.create_oval(165, 240, 175, 250, outline="blue", width=2)
            self.canvas.create_oval(180, 220, 195, 235, outline="blue", width=2)
            self.dibujar_ojos_muertos(170, 260)

    def dibujar_ojos_muertos(self, x, y):
        self.canvas.create_line(x, y, x+10, y+10, width=2, fill="black")
        self.canvas.create_line(x+10, y, x, y+10, width=2, fill="black")
        self.canvas.create_line(x+20, y, x+30, y+10, width=2, fill="black")
        self.canvas.create_line(x+30, y, x+20, y+10, width=2, fill="black")

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
                messagebox.showinfo("¡Ganaste!", f"¡Felicidades! La palabra era {self.palabra_secreta}. ¡El monito se salvó de la {self.tipo_muerte_actual}!")
                self.iniciar_juego()
        else:
            self.intentos += 1
            self.dibujar_progreso()
            if self.intentos >= self.max_intentos:
                msg = ""
                if self.tipo_muerte_actual == 'ahorcado': msg = "El monito ha sido ahorcado."
                elif self.tipo_muerte_actual == 'guillotina': msg = "¡CHOP! El monito perdió la cabeza."
                elif self.tipo_muerte_actual == 'hoguera': msg = "El monito terminó chamuscado."
                elif self.tipo_muerte_actual == 'ahogado': msg = "Glub glub... el monito se ahogó."
                
                messagebox.showerror("¡Perdiste!", f"{msg}\nLa palabra era {self.palabra_secreta}")
                self.iniciar_juego()

if __name__ == "__main__":
    root = tk.Tk()
    juego = AhorcadoJuego(root)
    root.mainloop()