import tkinter as tk
import random
import time

CELL = 28  # tamaño de cada celda en píxeles
ROWS = 21
COLS = 21

# Colores
BG = "#000000"       # fondo
WALL_COLOR = "#4DA3FF"  # pared pastel verde agua
DOT_COLOR = "#FFE1F0"   # puntos pastel rosado
PACMAN_COLOR = "#FFE27A" # amarillo pastel
GHOST_COLORS = ["#FF6F6F", "#FF9E6F", "#FFC36F", "#B56FFF"]
POWER_COLOR = "#FFD1D1"
TEXT_COLOR = "#333333"

# Mapa
# Diseño sencillo
MAP_TEMPLATE = [
    [1]*COLS,
]
for r in range(ROWS-2):
    row = [1] + [0]*(COLS-2) + [1]
    MAP_TEMPLATE.append(row)
MAP_TEMPLATE.append([1]*COLS)

# Paredes internas
for r in range(2, ROWS-2, 2):
    for c in range(2, COLS-2, 2):
        MAP_TEMPLATE[r][c] = 1

        dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        dx,dy = random.choice(dirs)
        MAP_TEMPLATE[r+dx][c+dy] = 1

# Fantasmas
center = ROWS//2
for r in range(center-1, center+2):
    for c in range(COLS//2-2, COLS//2+3):
        MAP_TEMPLATE[r][c] = 9

# Power pellets
pellet_positions = [(1,1),(1,COLS-2),(ROWS-2,1),(ROWS-2,COLS-2)]
for (r,c) in pellet_positions:
    MAP_TEMPLATE[r][c] = 2



class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Pacman XOXO")
        self.root.configure(bg=BG)
        self.canvas = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL, bg=BG, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=12, pady=12)

        self.score_var = tk.IntVar(value=0)
        self.lives_var = tk.IntVar(value=3)

        self.score_label = tk.Label(root, textvariable=self.score_var, bg=BG, fg=TEXT_COLOR, font=("Caviar Dreams", 12))
        self.score_label.grid(row=1, column=0, sticky="w", padx=12)
        self.lives_label = tk.Label(root, textvariable=self.lives_var, bg=BG, fg=TEXT_COLOR, font=("Caviar Dreams", 12))
        self.lives_label.grid(row=1, column=1)

        self.start_btn = tk.Button(root, text="Iniciar", command=self.start_game, bg=WALL_COLOR)
        self.start_btn.grid(row=1, column=2)
        self.reset_btn = tk.Button(root, text="Reiniciar", command=self.reset_game, bg=WALL_COLOR)
        self.reset_btn.grid(row=1, column=3, padx=12)

        self.root.bind("<KeyPress>", self.on_key)

        self.running = False
        self.build_map()
        self.draw()

    def build_map(self):
        
        self.map = [row[:] for row in MAP_TEMPLATE]
        
        for r in range(ROWS):
            for c in range(COLS):
                if self.map[r][c] == 0:
                    self.map[r][c] = 0  

        # Posicion_ini XO
        self.pacman_r = ROWS//2 + 3
        self.pacman_c = COLS//2
        self.pacman_dir = (0,0)
        self.score_var.set(0)
        self.lives_var.set(3)

        # Crear fantasmas
        self.ghosts = []
        ghost_start_positions = [(center, COLS//2-1), (center, COLS//2+1), (center-1, COLS//2), (center+1, COLS//2)]
        for i, pos in enumerate(ghost_start_positions):
            gr, gc = pos
            g = {
                'r': gr,
                'c': gc,
                'dir': random.choice([(0,1),(0,-1),(1,0),(-1,0)]),
                'color': GHOST_COLORS[i % len(GHOST_COLORS)],
                'vulnerable': False,
                'vul_timer': 0
            }
            self.ghosts.append(g)

        self.dots = 0
        for r in range(ROWS):
            for c in range(COLS):
                if self.map[r][c] == 0:
                    self.dots += 1
                elif self.map[r][c] == 2:
                    self.dots += 1

        self.tick_delay = 100
        self.power_mode = False
        self.power_timer = 0

    def reset_game(self):
        self.running = False
        self.build_map()
        self.canvas.delete("all")
        self.draw()

    def start_game(self):
        if not self.running:
            self.running = True
            self.game_loop()

    def draw(self):
        self.canvas.delete("all")
        # Dibujar map
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c*CELL
                y1 = r*CELL
                x2 = x1 + CELL
                y2 = y1 + CELL
                if self.map[r][c] == 1:
                    # Pared
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, width=0)
                elif self.map[r][c] == 0:
                    # Punto min
                    cx = x1 + CELL/2
                    cy = y1 + CELL/2
                    rdot = CELL*0.12
                    self.canvas.create_oval(cx-rdot, cy-rdot, cx+rdot, cy+rdot, fill=DOT_COLOR, outline=DOT_COLOR)
                elif self.map[r][c] == 2:
                    # Power pellet
                    cx = x1 + CELL/2
                    cy = y1 + CELL/2
                    rdot = CELL*0.26
                    self.canvas.create_oval(cx-rdot, cy-rdot, cx+rdot, cy+rdot, fill=POWER_COLOR, outline=POWER_COLOR)

        # Pacman XO
        px = self.pacman_c*CELL + CELL/2
        py = self.pacman_r*CELL + CELL/2
        r_p = CELL*0.42
        #'boca' 
        dx, dy = self.pacman_dir
        start = 30
        extent = 300
        if dx == 1:
            start = -30
        elif dx == -1:
            start = 150
        elif dy == 1:
            start = 60
        elif dy == -1:
            start = 240
        self.canvas.create_arc(px-r_p, py-r_p, px+r_p, py+r_p, start=start, extent=extent, fill=PACMAN_COLOR, outline=PACMAN_COLOR)

        # Fantasmas
        for g in self.ghosts:
            gx = g['c']*CELL + CELL/2
            gy = g['r']*CELL + CELL/2
            rr = CELL*0.42
            color = g['color']
            if g['vulnerable']:
                color = "#A8D0FF"  
            self.canvas.create_oval(gx-rr, gy-rr, gx+rr, gy+rr, fill=color, outline=color)
            # Ojo
            eye_r = CELL*0.09
            self.canvas.create_oval(gx-eye_r, gy-eye_r, gx+eye_r, gy+eye_r, fill="#FFFFFF", outline="#FFFFFF")

        # actualizar texto
        self.score_label.config(text=f"Puntuación: {self.score_var.get()}")
        self.lives_label.config(text=f"Vidas: {self.lives_var.get()}")

    def on_key(self, event):
        k = event.keysym
        if k == 'Left':
            self.pacman_dir = (0,-1)
        elif k == 'Right':
            self.pacman_dir = (0,1)
        elif k == 'Up':
            self.pacman_dir = (-1,0)
        elif k == 'Down':
            self.pacman_dir = (1,0)
        elif k == 'space':
            if not self.running:
                self.start_game()

    def valid(self, r, c):
        return 0 <= r < ROWS and 0 <= c < COLS and self.map[r][c] != 1

    def step_pacman(self):
        dr, dc = self.pacman_dir
        nr = self.pacman_r + dr
        nc = self.pacman_c + dc
        if self.valid(nr, nc):
            self.pacman_r = nr
            self.pacman_c = nc
            cell = self.map[nr][nc]
            if cell == 0:
                self.score_var.set(self.score_var.get() + 10)
                self.map[nr][nc] = 9
                self.dots -= 1
            elif cell == 2:
                self.score_var.set(self.score_var.get() + 50)
                self.map[nr][nc] = 9
                self.dots -= 1
                self.activate_power()

    def activate_power(self):
        self.power_mode = True
        self.power_timer = 60  
        for g in self.ghosts:
            g['vulnerable'] = True
            g['vul_timer'] = self.power_timer

    def step_ghosts(self):
        for g in self.ghosts:
            # Temp
            if g['vulnerable']:
                g['vul_timer'] -= 1
                if g['vul_timer'] <= 0:
                    g['vulnerable'] = False

            # Movim
            r, c = g['r'], g['c']
            dr, dc = g['dir']
            # Intersección, elegir nueva dirección válida al azar
            ahead_r, ahead_c = r+dr, c+dc
            if not self.valid(ahead_r, ahead_c) or (random.random() < 0.25):
                choices = []
                for d in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = r+d[0], c+d[1]
                    if self.valid(nr, nc):
                        choices.append(d)
                if choices:
                    g['dir'] = random.choice(choices)
                    dr, dc = g['dir']
            # Mov
            g['r'] += dr
            g['c'] += dc

    def check_collisions(self):
        for g in self.ghosts:
            if g['r'] == self.pacman_r and g['c'] == self.pacman_c:
                if g['vulnerable']:
                    self.score_var.set(self.score_var.get() + 200)
                    g['r'], g['c'] = center, COLS//2
                    g['vulnerable'] = False
                else:
                    # Vida
                    self.lives_var.set(self.lives_var.get() - 1)
                    if self.lives_var.get() <= 0:
                        self.game_over()
                    else:
                        self.pacman_r = ROWS//2 + 3
                        self.pacman_c = COLS//2
                        for i, gg in enumerate(self.ghosts):
                            gg['r'], gg['c'] = ghost_start_positions[i]
                    break

    def game_over(self):
        self.running = False
        self.canvas.create_text(COLS*CELL/2, ROWS*CELL/2, text="GAME OVER", font=("Caviar Dreams", 32, "bold"), fill=TEXT_COLOR)

    def game_win(self):
        self.running = False
        self.canvas.create_text(COLS*CELL/2, ROWS*CELL/2, text="YOU WIN!", font=("Caviar Dreams", 32, "bold"), fill=TEXT_COLOR)

    def game_loop(self):
        if not self.running:
            return
        self.step_pacman()
        self.step_ghosts()
        self.check_collisions()
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                for g in self.ghosts:
                    g['vulnerable'] = False
        if self.dots <= 0:
            self.game_win()
            return
        self.draw()
        self.root.after(self.tick_delay, self.game_loop)


if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    root.mainloop()