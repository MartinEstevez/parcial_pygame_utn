import pygame
from configuraciones import *
import csv

ruta_csv = "puntajes.csv"

def dibujar_boton(pantalla: pygame.Surface, rect_boton: pygame.Rect, texto: str, fuente: pygame.font.Font, color_fondo=COLOR_FONDO_BOTON, color_texto=COLOR_TEXTO):
    """Dibuja un botón en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el botón.
        rect_boton (pygame.Rect): El rectángulo que define la posición y tamaño del botón.
        texto (str): El texto a mostrar en el botón.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
        color_fondo (tuple, optional): El color de fondo del botón. 
        color_texto (tuple, optional): El color del texto.
    """
    pygame.draw.rect(pantalla, color_fondo, rect_boton)
    texto_render = fuente.render(texto, True, color_texto)
    rect_texto = texto_render.get_rect(center=rect_boton.center)
    pantalla.blit(texto_render, rect_texto)

def dibujar_titulo(pantalla: pygame.Surface, texto: str, fuente: pygame.font.Font, ancho_pantalla: int):
    """Dibuja un título en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el título.
        texto (str): El texto del título.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
        ancho_pantalla (int): El ancho de la pantalla.
    """
    titulo_render = fuente.render(texto, True, COLOR_TEXTO)
    x_titulo = (ancho_pantalla - titulo_render.get_width()) / 2
    pantalla.blit(titulo_render, (x_titulo, 60))

def dibujar_botones_menu(pantalla: pygame.Surface, textos: list, fuente: pygame.font.Font, y_inicial: int, ancho_boton: int, alto_boton: int, espacio: int, ancho_pantalla: int):
    """Dibuja los botones del menú en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujarán los botones.
        textos (list): La lista de textos para los botones.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
        y_inicial (int): La posición vertical inicial para los botones.
        ancho_boton (int): El ancho de los botones.
        alto_boton (int): La altura de los botones.
        espacio (int): El espacio entre los botones.
        ancho_pantalla (int): El ancho de la pantalla.

    Returns:
        list: La lista de rectángulos de los botones dibujados.
    """
    botones = []
    for i in range(len(textos)):
        x = (ancho_pantalla - ancho_boton) / 2
        y = y_inicial + i * (alto_boton + espacio)
        rect = pygame.Rect(x, y, ancho_boton, alto_boton)
        dibujar_boton(pantalla, rect, textos[i], fuente)
        botones.append(rect)
    return botones

def dibujar_respuestas(pantalla: pygame.Surface, respuestas: list, fuente: pygame.font.Font):
    """Dibuja los botones de respuesta en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujarán los botones.
        respuestas (list): La lista de respuestas a mostrar.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.

    Returns:
        list: La lista de rectángulos de los botones dibujados.
    """
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
    """Dibuja un temporizador en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el temporizador.
        segundos (int): El tiempo en segundos a mostrar.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
    """
    
    min = segundos // 60
    seg = segundos % 60
    texto_timer = fuente.render(f"{min:02}:{seg:02}", True, COLOR_TEXTO)
    rect_texto = texto_timer.get_rect(center=(ANCHO_PANTALLA // 2, 40))
    rect_fondo = pygame.Rect(rect_texto.left - 10, rect_texto.top - 5, rect_texto.width + 20, rect_texto.height + 10)
    pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect_fondo, border_radius=10)
    pygame.draw.rect(pantalla, COLOR_BORDE_TIMER, rect_fondo, 2, border_radius=10)
    pantalla.blit(texto_timer, rect_texto)

def dibujar_pregunta(pantalla: pygame.Surface, texto: str, fuente: pygame.font.Font):
    """Dibuja una pregunta en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará la pregunta.
        texto (str): El texto de la pregunta.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
    """
    x = ANCHO_PANTALLA * 0.125
    y = ALTO_PANTALLA * 0.167
    ancho = ANCHO_PANTALLA * 0.75
    alto = ALTO_PANTALLA * 0.1

    rect_pregunta = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect_pregunta, border_radius=15)

    texto_render = fuente.render(texto, True, COLOR_TEXTO)
    pantalla.blit(texto_render, texto_render.get_rect(center=rect_pregunta.center))

def dibujar_reset(pantalla: pygame.Surface, icono_reset: pygame.Surface):
    """Dibuja el botón de reinicio en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el botón de reinicio.
        icono_reset (pygame.Surface): El ícono que se mostrará en el botón de reinicio.

    Returns:
        pygame.Rect: El rectángulo que define la posición y tamaño del botón de reinicio.
    """
    ancho = ANCHO_PANTALLA * 0.056
    alto = ALTO_PANTALLA * 0.075
    x = ANCHO_PANTALLA * 0.012
    y = ALTO_PANTALLA * 0.015

    rect_reset = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect_reset)
    pygame.draw.rect(pantalla, COLOR_BORDE_TIMER, rect_reset, 2)

    ancho_img = ANCHO_PANTALLA * 0.0375
    alto_img = ALTO_PANTALLA * 0.05
    x_img = x + (ancho - ancho_img) / 2
    y_img = y + (alto - alto_img) / 2

    pantalla.blit(icono_reset, pygame.Rect(x_img, y_img, ancho_img, alto_img))
    return rect_reset

def dibujar_boton_volver(pantalla: pygame.Surface, fuente: pygame.font.Font):
    """Dibuja el botón de volver en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el botón de volver.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.

    Returns:
        rect_volver: El rectángulo que define la posición y tamaño del botón de volver.
    """
    ancho_boton = int(ANCHO_PANTALLA * 0.18)
    alto_boton = int(ALTO_PANTALLA * 0.07)
    x = ANCHO_PANTALLA - ancho_boton - int(ANCHO_PANTALLA * 0.02)
    y = ALTO_PANTALLA - alto_boton - int(ALTO_PANTALLA * 0.12)
    rect_volver = pygame.Rect(x, y, ancho_boton, alto_boton)
    dibujar_boton(pantalla, rect_volver, "VOLVER", fuente)
    return rect_volver

def dibujar_fondo_por_pantalla(pantalla: pygame.Surface, pantalla_actual: str):
    """Dibuja el fondo correspondiente a la pantalla actual.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará el fondo.
        pantalla_actual (str): El estado actual de la pantalla.
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

def dibujar_comodines(pantalla: pygame.Surface, imagenes: list[pygame.Surface]):
    """Dibuja los comodines (imágenes) centrados abajo y devuelve una lista de sus rectángulos.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujarán los comodines.
        imagenes (int): Lista de imágenes de los comodines.

    Returns:
        botones: Lista de rectángulos que representan los botones de los comodines.
    """
    botones = []
    cantidad = len(imagenes)
    if cantidad == 0:
        return botones
    ancho = imagenes[0].get_width()
    alto = imagenes[0].get_height()
    espacio = 40
    ancho_total = ancho * cantidad + espacio * (cantidad - 1)
    x_inicial = (ANCHO_PANTALLA - ancho_total) // 2
    y = ALTO_PANTALLA - alto - 20

    for i in range(cantidad):
        x = x_inicial + i * (ancho + espacio)
        rect = pygame.Rect(x, y, ancho, alto)
        pantalla.blit(imagenes[i], rect)
        botones.append(rect)
    return botones

def leer_puntajes_csv(ruta_csv: str) -> list[dict]:
    """Lee un archivo CSV de puntajes y devuelve una lista de diccionarios.

    Args:
        ruta_csv (str): La ruta del archivo CSV a leer.

    Returns:
        list[dict]: Una lista de diccionarios con los puntajes leídos del CSV.
    """
    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def dibujar_tabla_puntajes(pantalla: pygame.Surface, puntajes: list[dict], fuente: pygame.font.Font):
    """Dibuja una tabla de puntajes en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujará la tabla.
        puntajes (list[dict]): La lista de diccionarios con los puntajes.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
    """
    encabezados = ["Nombre", "Puntaje"]
    x_inicial = ANCHO_PANTALLA * 0.2
    y_inicial = ALTO_PANTALLA * 0.22
    ancho_columna = ANCHO_PANTALLA * 0.3
    alto_fila = ALTO_PANTALLA * 0.06
    espacio = ALTO_PANTALLA * 0.01
    color_fondo = (0, 0, 0)
    color_linea = (255, 255, 255)
    color_texto_puntaje = (0, 0, 0)

    filas = len(puntajes) + 1  # +1 por encabezado

    # Fondo de la tabla
    ancho_tabla = 2 * ancho_columna + espacio
    alto_tabla = filas * (alto_fila + espacio)
    pygame.draw.rect(pantalla, color_fondo, (x_inicial - 2, y_inicial - 2, ancho_tabla + 4, alto_tabla + 2))

    # Encabezados
    for i in range(len(encabezados)):
        rect = pygame.Rect(x_inicial + i * (ancho_columna + espacio), y_inicial, ancho_columna, alto_fila)
        pygame.draw.rect(pantalla, color_linea, rect)
        texto = fuente.render(encabezados[i], True, color_texto_puntaje)
        pantalla.blit(texto, texto.get_rect(center=rect.center))

    # Filas de puntajes
    for fila in range(len(puntajes)):
        y = y_inicial + (fila + 1) * (alto_fila + espacio)
        jugador = puntajes[fila]
        # Nombre
        rect_nombre = pygame.Rect(x_inicial, y, ancho_columna, alto_fila)
        pygame.draw.rect(pantalla, color_linea, rect_nombre)
        texto_nombre = fuente.render(jugador["nombre"], True, color_texto_puntaje)
        pantalla.blit(texto_nombre, texto_nombre.get_rect(center=rect_nombre.center))
        # Puntaje
        rect_puntaje = pygame.Rect(x_inicial + ancho_columna + espacio, y, ancho_columna, alto_fila)
        pygame.draw.rect(pantalla, color_linea, rect_puntaje)
        texto_puntaje = fuente.render(jugador["puntaje"], True, color_texto_puntaje)
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(center=rect_puntaje.center))

def dibujar_marcadores(pantalla: pygame.Surface, puntaje_total: int, respuestas_correctas: int, preguntas_respondidas: int, fuente: pygame.font.Font, color_fondo: tuple, color_texto: tuple):
    """Dibuja los marcadores de puntaje y porcentaje en la esquina inferior izquierda,con un rectángulo de fondo sencillo.

    Args:
        pantalla (pygame.Surface): La superficie donde se dibujarán los marcadores.
        puntaje_total (int): El puntaje total del jugador.
        respuestas_correctas (int): La cantidad de respuestas correctas.
        preguntas_respondidas (int): La cantidad de preguntas respondidas.
        fuente (pygame.font.Font): La fuente a utilizar para el texto.
        color_fondo (tuple): El color de fondo del rectángulo.
        color_texto (tuple): El color del texto.
    """
    marcador_puntaje = fuente.render(f"PUNTAJE = {puntaje_total}", True, color_texto)
    if preguntas_respondidas > 0:
        porcentaje = int((respuestas_correctas / preguntas_respondidas) * 100)
    else:
        porcentaje = 0
    marcador_porcentaje = fuente.render(f"% CORRECTAS = {porcentaje} %", True, color_texto)

    x = int(pantalla.get_width() * 0.02)
    y = int(pantalla.get_height() * 0.82)

    # Calcula el ancho y alto del rectángulo según los textos
    ancho = max(marcador_puntaje.get_width(), marcador_porcentaje.get_width()) + 5
    alto = marcador_puntaje.get_height() + marcador_porcentaje.get_height() + 5

    # Dibuja el rectángulo de fondo
    pygame.draw.rect(pantalla, color_fondo, (x - 5, y - 5, ancho, alto))
    pygame.draw.rect(pantalla, (180, 180, 180), (x - 5, y - 5, ancho, alto), 2)

    # Dibuja los textos encima
    pantalla.blit(marcador_puntaje, (x, y))
    pantalla.blit(marcador_porcentaje, (x, y + marcador_puntaje.get_height()))

