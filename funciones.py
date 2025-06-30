import pygame
from configuraciones import *

def dibujar_boton(pantalla: pygame.Surface, rect_boton: pygame.Rect, texto: str, fuente: pygame.font.Font, color_fondo=COLOR_FONDO_BOTON, color_texto=COLOR_TEXTO):
    pygame.draw.rect(pantalla, color_fondo, rect_boton, border_radius=10)
    texto_render = fuente.render(texto, True, color_texto)
    rect_texto = texto_render.get_rect(center=rect_boton.center)
    pantalla.blit(texto_render, rect_texto)

def dibujar_titulo(pantalla: pygame.Surface, texto: str, fuente: pygame.font.Font, ancho_pantalla: int):
    titulo_render = fuente.render(texto, True, COLOR_TEXTO)
    x_titulo = (ancho_pantalla - titulo_render.get_width()) / 2
    pantalla.blit(titulo_render, (x_titulo, 120))

def dibujar_botones_menu(pantalla: pygame.Surface, textos: list, fuente: pygame.font.Font, y_inicial: int, ancho_boton: int, alto_boton: int, espacio: int, ancho_pantalla: int):
    botones = []
    for i in range(len(textos)):
        x = (ancho_pantalla - ancho_boton) / 2
        y = y_inicial + i * (alto_boton + espacio)
        rect = pygame.Rect(x, y, ancho_boton, alto_boton)
        dibujar_boton(pantalla, rect, textos[i], fuente)
        botones.append(rect)
    return botones

def dibujar_respuestas(pantalla: pygame.Surface, respuestas: list, fuente: pygame.font.Font):

    espacio_vertical = ALTO_PANTALLA * 0.05
    botones = []

    posicion_x = [ANCHO_PANTALLA * 0.10, ANCHO_PANTALLA * 0.55]
    posicion_y = ALTO_PANTALLA * 0.35

    for i in range(len(respuestas)):
        fila = i // 2
        columna = i % 2
        x = posicion_x[columna]
        y = posicion_y + fila * (ALTO_BOTON + espacio_vertical)
        rect = pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON)
        dibujar_boton(pantalla, rect, respuestas[i], fuente)
        botones.append(rect)

    return botones

def dibujar_timer(pantalla: pygame.Surface, segundos: int, fuente: pygame.font.Font):
    min = segundos // 60
    seg = segundos % 60
    texto_timer = fuente.render(f"{min:02}:{seg:02}", True, COLOR_TEXTO)
    rect_texto = texto_timer.get_rect(center=(ANCHO_PANTALLA // 2, 40))
    rect_fondo = pygame.Rect(rect_texto.left - 10, rect_texto.top - 5, rect_texto.width + 20, rect_texto.height + 10)
    pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect_fondo, border_radius=10)
    pygame.draw.rect(pantalla, COLOR_BORDE_TIMER, rect_fondo, 2, border_radius=10)
    pantalla.blit(texto_timer, rect_texto)

def dibujar_pregunta(pantalla: pygame.Surface, texto: str, fuente: pygame.font.Font):
    x = ANCHO_PANTALLA * 0.125
    y = ALTO_PANTALLA * 0.167
    ancho = ANCHO_PANTALLA * 0.75
    alto = ALTO_PANTALLA * 0.1

    rect_pregunta = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect_pregunta, border_radius=15)

    texto_render = fuente.render(texto, True, COLOR_TEXTO)
    pantalla.blit(texto_render, texto_render.get_rect(center=rect_pregunta.center))

def dibujar_reset(pantalla: pygame.Surface, icono_reset: pygame.Surface):
    ancho = ANCHO_PANTALLA * 0.056
    alto = ALTO_PANTALLA * 0.075
    x = ANCHO_PANTALLA * 0.012
    y = ALTO_PANTALLA * 0.015

    rect_reset = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect_reset, border_radius=10)
    pygame.draw.rect(pantalla, COLOR_BORDE_TIMER, rect_reset, 2, border_radius=10)

    ancho_img = ANCHO_PANTALLA * 0.0375
    alto_img = ALTO_PANTALLA * 0.05
    x_img = x + (ancho - ancho_img) / 2
    y_img = y + (alto - alto_img) / 2

    pantalla.blit(icono_reset, pygame.Rect(x_img, y_img, ancho_img, alto_img))

def dibujar_boton_volver(pantalla: pygame.Surface, fuente: pygame.font.Font):
    rect_volver = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
    dibujar_boton(pantalla, rect_volver, "VOLVER", fuente)
    return rect_volver

def dibujar_fondo_por_pantalla(pantalla: pygame.Surface, pantalla_actual: str):
    """
    Carga y dibuja el fondo correspondiente a la pantalla actual.
    """
    if pantalla_actual == "EN_JUEGO":
        ruta = RUTA_IMAGEN_FONDO_JUEGO
    elif pantalla_actual == "PEDIR_NOMBRE":
        ruta = RUTA_IMAGEN_FONDO_JUEGO
    elif pantalla_actual == "CONFIGURACIÓN":
        ruta = RUTA_IMAGEN_FONDO_CONFIG
    elif pantalla_actual == "PUNTAJES":
        ruta = RUTA_IMAGEN_FONDO_PUNTAJES
    else:
        ruta = RUTA_IMAGEN_MENU

    fondo = pygame.transform.scale(pygame.image.load(ruta), (ANCHO_PANTALLA, ALTO_PANTALLA))
    pantalla.blit(fondo, (0, 0))

def dibujar_comodines(pantalla: pygame.Surface, nombres: list, fuente: pygame.font.Font) -> list[pygame.Rect]:
    """
    Dibuja los botones de comodines centrados abajo y devuelve sus rectángulos.
    """
    botones = []
    ancho_total = (ANCHO_BOTON * len(nombres)) + ESPACIO_ENTRE_BOTONES * (len(nombres) - 1)
    x_inicial = (ANCHO_PANTALLA - ancho_total) / 2
    y = ALTO_PANTALLA - 120

    for i in range(len(nombres)):
        x = x_inicial + i * (ANCHO_BOTON + ESPACIO_ENTRE_BOTONES)
        rect = pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON)
        dibujar_boton(pantalla, rect, nombres[i], fuente)
        botones.append(rect)

    return botones





