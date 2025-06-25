import pygame
from configuraciones import *
from funciones import *

pygame.init() # INICIALIZAMOS PYGAME
pygame.mixer.init() # INICIALIZAMOS EL MÓDULO DE SONIDO

# PANTALLA
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA)) # CREAMOS LA PANTALLA
pygame.display.set_caption(TITULO_JUEGO) # TÍTULO DEL JUEGO
pygame.display.set_icon(pygame.image.load(RUTA_FAVICON)) # CARGANDO EL FAVICON

# FUENTES
fuente_titulo = pygame.font.SysFont("timesnewroman", TAM_FUENTE_TITULO)
fuente_boton = pygame.font.SysFont("timesnewroman", TAM_FUENTE_BOTON)
fuente_des = pygame.font.SysFont("timesnewroman", TAM_FUENTE_DES)
fuente_timer = pygame.font.SysFont("timesnewroman", TAM_FUENTE_TIMER)
fuente_pregunta = pygame.font.SysFont("timesnewroman", TAM_FUENTE_PREGUNTA)

# ICONOS
icono_sonido_on = pygame.transform.scale(pygame.image.load(RUTA_ICONO_SONIDO_ON), (40, 40)) # Escalando el icono de sonido ON
icono_sonido_off = pygame.transform.scale(pygame.image.load(RUTA_ICONO_SONIDO_OFF), (40, 40)) # Escalando el icono de sonido OFF
icono_reset = pygame.transform.scale(pygame.image.load(RUTA_ICONO_RESET), (30, 30)) # Escalando el icono de reset
rect_icono_sonido = icono_sonido_on.get_rect(topright=(ANCHO_PANTALLA, 10)) # Posicionando el icono de sonido en la esquina superior derecha

# MÚSICA
pygame.mixer.music.load(RUTA_MUSICA_MENU) # CARGANDO LA MÚSICA DEL MENÚ
pygame.mixer.music.play(-1) # REPRODUCIENDO LA MÚSICA EN BUCLE
pygame.mixer.music.set_volume(0.5) # VOLUMEN DE LA MÚSICA

# TIMER
evento_tick = pygame.USEREVENT + 3
pygame.time.set_timer(evento_tick, 1000) # POR SEGUNDO
segundos = 0


pantalla_actual = "MENU"
musica_activa = True

# BOTONES PARA MENU
botones_menu = ["JUGAR", "PUNTAJES", "CONFIGURACIÓN", "SALIR"]
botones_configuracion = ["DIMENSIONES", "SONIDO", "VOLVER"]


pregunta = "¿Cuál es la capital de Francia?"
respuestas = ["Madrid", "París", "Roma", "Londres",]

desarrolladores = ["Martín Estevez", "Nicolas Rial Dell Anna", "Tomas Gil"]

# BUCLE PRINCIPAL
corriendo = True

while corriendo:
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            corriendo = False  # Salir del bucle y cerrar el juego

        if evento.type == evento_tick:
            if pantalla_actual == "EN_JUEGO":
                segundos += 1

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if rect_icono_sonido.collidepoint(mouse_pos):
                    if musica_activa == True:
                        musica_activa = False
                        pygame.mixer.music.set_volume(0.0)
                    else:
                        musica_activa = True
                        pygame.mixer.music.set_volume(0.5)

            if pantalla_actual == "MENU":
                x = (ANCHO_PANTALLA - ANCHO_BOTON) / 2

                for i in range(len(botones_menu)): 
                    y = Y_BOTONES + i * (ALTO_BOTON + ESPACIO_ENTRE_BOTONES)
                    
                    if pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON).collidepoint(mouse_pos):

                        if botones_menu[i] == "SALIR":
                            corriendo = False
                        elif botones_menu[i] == "JUGAR":
                            pantalla_actual = "EN_JUEGO"
                            segundos = 0 # Reiniciar el contador de segundos al iniciar el juego
                        elif botones_menu[i] == "CONFIGURACIÓN":
                            pantalla_actual = "CONFIGURACIÓN"

            elif pantalla_actual == "CONFIGURACIÓN":
                x = (ANCHO_PANTALLA - ANCHO_BOTON) / 2
                for i in range(len(botones_configuracion)):
                    
                    y = Y_BOTONES + i * (ALTO_BOTON + ESPACIO_ENTRE_BOTONES)

                    if pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON).collidepoint(mouse_pos):
                        if botones_configuracion[i] == "VOLVER":
                            pantalla_actual = "MENU"

            elif pantalla_actual == "EN_JUEGO":
                volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)

                if volver_rect.collidepoint(mouse_pos):
                    pantalla_actual = "MENU"

                if pygame.Rect(10, 10, 45, 45).collidepoint(mouse_pos):
                    segundos = 0

    fondo = pygame.image.load(RUTA_IMAGEN_MENU if pantalla_actual != "EN_JUEGO" else RUTA_IMAGEN_FONDO_JUEGO)

    fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    
    pantalla.blit(fondo, (0, 0))

    if pantalla_actual == "MENU":
        dibujar_titulo(pantalla, "MENÚ PRINCIPAL", fuente_titulo, ANCHO_PANTALLA)
        dibujar_botones_menu(pantalla, botones_menu, fuente_boton, Y_BOTONES, ANCHO_BOTON, ALTO_BOTON, ESPACIO_ENTRE_BOTONES, ANCHO_PANTALLA)

        for i in range(len(desarrolladores)):
            texto = fuente_des.render(desarrolladores[i], True, COLOR_TEXTO)
            pantalla.blit(texto, (10, ALTO_PANTALLA - 120 + i * 30))

    elif pantalla_actual == "CONFIGURACIÓN":
        dibujar_titulo(pantalla, "CONFIGURACIÓN", fuente_titulo, ANCHO_PANTALLA)
        dibujar_botones_menu(pantalla, botones_configuracion, fuente_boton, Y_BOTONES, ANCHO_BOTON, ALTO_BOTON, ESPACIO_ENTRE_BOTONES, ANCHO_PANTALLA)

    elif pantalla_actual == "EN_JUEGO":
        dibujar_timer(pantalla, segundos, fuente_timer)

        dibujar_reset(pantalla, icono_reset)
        dibujar_pregunta(pantalla, pregunta, fuente_pregunta)

        # Dibuja las respuestas con la nueva función
        dibujar_respuestas(pantalla, respuestas, fuente_boton)

        dibujar_boton(pantalla, pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40), "VOLVER", fuente_boton)

    pantalla.blit(icono_sonido_on if musica_activa else icono_sonido_off, rect_icono_sonido)
    pygame.display.update()

pygame.quit()
