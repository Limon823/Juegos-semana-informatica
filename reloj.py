import pygame
import math
import sys
import random

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reloj Simple")
reloj = pygame.time.Clock()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

centro_x, centro_y = 400, 300
radio = 150
angulo = 0
velocidad = 0.05
jugando = True
angulo_meta = random.uniform(0, 6.28)

while True:
    x = centro_x + math.cos(angulo) * radio
    y = centro_y + math.sin(angulo) * radio
    
    x_meta = centro_x + math.cos(angulo_meta) * radio
    y_meta = centro_y + math.sin(angulo_meta) * radio

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if jugando:
                    distancia = math.dist((x, y), (x_meta, y_meta))
                    if distancia < 30:
                        angulo_meta = random.uniform(0, 6.28)
                    jugando = False
                else:
                    jugando = True

    if jugando:
        angulo += velocidad
        if angulo > 6.28:
            angulo = 0

    pantalla.fill(NEGRO)

    pygame.draw.circle(pantalla, BLANCO, (centro_x, centro_y), radio, 2)
    pygame.draw.circle(pantalla, AZUL, (int(x_meta), int(y_meta)), 20)

    color_jugador = ROJO
    if math.dist((x, y), (x_meta, y_meta)) < 30:
        color_jugador = VERDE

    pygame.draw.circle(pantalla, color_jugador, (int(x), int(y)), 15)

    pygame.display.flip()
    reloj.tick(60)
