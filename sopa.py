# Perez Limón Alejandro harbel
# 1301 LI 
import tkinter as tk
import random
import string

TAMAÑO = 10
DIRECCIONES = [(1,0),(0,1),(1,1),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1)]
ALFABETO = string.ascii_uppercase 
MAX_PALABRAS = 5

class AppSopaDeLetras:
    def __init__(self): 
        self.palabras=[]
        self.celdas=[[None]*TAMAÑO for _ in range(TAMAÑO)]
        self.celdas_seleccionadas = [] 

    def iniciarInterfaz(self, v):
        self.v=v
        v.title("limon - Sopa de Letras"); v.resizable(0,0);
        p_juego=tk.Frame(v); p_juego.pack(side=tk.LEFT, padx=5, pady=5)
        p_info=tk.Frame(v); p_info.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)
        
        for r in range(TAMAÑO):
            for c in range(TAMAÑO):
                self.celdas[r][c]=tk.Label(p_juego,text=' ',width=2,height=1,borderwidth=1,relief="solid",font=('Arial',10))
                self.celdas[r][c].grid(row=r,column=c,padx=0,pady=0)
                self.celdas[r][c].bind("<Button-1>", lambda e, r=r, c=c: self.manejar_clic_celda(r, c))
                
        tk.Label(p_info,text="Tus Palabras",font=('Arial',12,'bold')).pack(pady=(5,5))
        tk.Label(p_info,text=f"Máximo {MAX_PALABRAS}. Separar con coma:").pack(anchor='w')
        self.e=tk.Entry(p_info,width=30); self.e.pack(fill=tk.X,pady=(0,10))
        tk.Label(p_info,text="PALABRAS A BUSCAR:",font=('Arial',10,'bold')).pack(anchor='w',pady=(10,5))
        self.l=tk.Label(p_info,text="Ingresa tus palabras",justify=tk.LEFT); self.l.pack(anchor='w')
        tk.Button(p_info,text="Generar Nueva Sopa",command=self.manejarGeneracion).pack(pady=20,fill=tk.X)

    def manejarGeneracion(self):
        p_temp=[p.strip().upper() for p in self.e.get().replace(',',' ').split() if p.strip()]
        p_temp = [p for p in p_temp if len(p) <= TAMAÑO]
        
        if len(p_temp)>MAX_PALABRAS: 
            p_temp = p_temp[:MAX_PALABRAS]
        
        if not p_temp: 
            self.palabras = []
            self.l.config(text="Ninguna palabra válida")
            self.celdas_seleccionadas = []
            self.actualizarVista([[' ']*TAMAÑO for _ in range(TAMAÑO)]) 
            return 
            
        self.palabras=p_temp
        self.l.config(text='\n'.join(self.palabras))
        self.celdas_seleccionadas = []
        self.generar_sopa()

    def generar_sopa(self):
        s=[[' ']*TAMAÑO for _ in range(TAMAÑO)]
        for p in self.palabras: 
            colocado=False; intentos=0
            while not colocado and intentos<500:
                intentos+=1
                r_i=random.randint(0,TAMAÑO-1); c_i=random.randint(0,TAMAÑO-1)
                dr,dc=random.choice(DIRECCIONES)
                r_f=r_i+(len(p)-1)*dr; c_f=c_i+(len(p)-1)*dc
                if 0<=r_f<TAMAÑO and 0<=c_f<TAMAÑO:
                    cabe=True
                    for i,letra in enumerate(p):
                        r=r_i+i*dr; c=c_i+i*dc
                        if s[r][c]!=' ' and s[r][c]!=letra: cabe=False; break
                    if cabe:
                        for i,letra in enumerate(p): s[r_i+i*dr][c_i+i*dc]=letra
                        colocado=True
                        
        for r in range(TAMAÑO):
            for c in range(TAMAÑO):
                if s[r][c]==' ': s[r][c]=random.choice(ALFABETO)
                
        self.actualizarVista(s) 

    def actualizarVista(self,d):
        for r in range(TAMAÑO):
            for c in range(TAMAÑO):
                self.celdas[r][c].config(text=d[r][c], bg='SystemButtonFace')

    def manejar_clic_celda(self, r, c):
        celda = self.celdas[r][c]
        coordenada = (r, c)
        
        if coordenada in self.celdas_seleccionadas:
            celda.config(bg='SystemButtonFace')
            self.celdas_seleccionadas.remove(coordenada)
        else:
            celda.config(bg='green')
            self.celdas_seleccionadas.append(coordenada)
v=tk.Tk()
app=AppSopaDeLetras()
app.iniciarInterfaz(v) 
v.mainloop()