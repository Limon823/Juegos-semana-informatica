import pygame
import math
import sys
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Reloj")
reloj = pygame.time.Clock()

FONDO = (5, 5, 12)
NEON_ORANGE = (255, 100, 0)
NEON_CYAN = (0, 240, 255)
NEON_BLANCO = (200, 255, 255)
NEON_ROJO = (255, 50, 50)

centro_x = ANCHO // 2
centro_y = ALTO // 2
radio = 180
angulo = 4.71
velocidad = 0.05
girando = True
angulo_meta = random.uniform(0, 6.28)

cola_posiciones = []

def dibujar_resplandor(superficie, color, pos, radio_brillo):
    s = pygame.Surface((radio_brillo*4, radio_brillo*4), pygame.SRCALPHA)
    pygame.draw.circle(s, (*color, 40), (radio_brillo*2, radio_brillo*2), radio_brillo)
    pygame.draw.circle(s, (*color, 80), (radio_brillo*2, radio_brillo*2), radio_brillo // 1.5)
    superficie.blit(s, (pos[0] - radio_brillo*2, pos[1] - radio_brillo*2))

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if girando:
                    girando = False
                else:
                    girando = True
                    angulo = 4.71
                    angulo_meta = random.uniform(0, 6.28)
                    cola_posiciones.clear()

    if girando:
        angulo += velocidad
        if angulo > 6.28:
            angulo -= 6.28
    
    x_bola = centro_x + math.cos(angulo) * radio
    y_bola = centro_y + math.sin(angulo) * radio
    
    x_meta = centro_x + math.cos(angulo_meta) * radio
    y_meta = centro_y + math.sin(angulo_meta) * radio

    pantalla.fill(FONDO)

    pygame.draw.circle(pantalla, (20, 25, 40), (centro_x, centro_y), radio - 20)
    pygame.draw.circle(pantalla, (40, 50, 70), (centro_x, centro_y), radio, 2)

    dibujar_resplandor(pantalla, NEON_ORANGE, (int(x_meta), int(y_meta)), 30)
    pygame.draw.circle(pantalla, NEON_ORANGE, (int(x_meta), int(y_meta)), 15)
    pygame.draw.circle(pantalla, NEON_BLANCO, (int(x_meta), int(y_meta)), 6)

    if girando:
        cola_posiciones.append((x_bola, y_bola))
        if len(cola_posiciones) > 20:
            cola_posiciones.pop(0)

    for i, pos in enumerate(cola_posiciones):
        alfa = int(255 * (i / len(cola_posiciones)))
        sz = int(18 * (i / len(cola_posiciones)))
        s_trail = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(s_trail, (*NEON_CYAN, alfa), (20, 20), sz)
        pantalla.blit(s_trail, (pos[0]-20, pos[1]-20))

    color_jugador = NEON_CYAN
    if not girando:
        distancia = abs(math.atan2(math.sin(angulo - angulo_meta), math.cos(angulo - angulo_meta)))
        if distancia < 0.15:
            color_jugador = (50, 255, 50)
            dibujar_resplandor(pantalla, color_jugador, (int(x_bola), int(y_bola)), 60)
        else:
            color_jugador = NEON_ROJO
            dibujar_resplandor(pantalla, color_jugador, (int(x_bola), int(y_bola)), 50)
    else:
        dibujar_resplandor(pantalla, NEON_CYAN, (int(x_bola), int(y_bola)), 30)

    pygame.draw.circle(pantalla, color_jugador, (int(x_bola), int(y_bola)), 12)
    pygame.draw.circle(pantalla, NEON_BLANCO, (int(x_bola), int(y_bola)), 5)

    pygame.display.flip()
    reloj.tick(130)