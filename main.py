import pygame
from configuraciones import *
from funciones import *
from funciones_respuestas import *

pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(TITULO_JUEGO)
pygame.display.set_icon(pygame.image.load(RUTA_FAVICON))

# FUENTES
fuente_titulo = pygame.font.SysFont("timesnewroman", TAM_FUENTE_TITULO)
fuente_boton = pygame.font.SysFont("timesnewroman", TAM_FUENTE_BOTON)
fuente_des = pygame.font.SysFont("timesnewroman", TAM_FUENTE_DES)
fuente_timer = pygame.font.SysFont("timesnewroman", TAM_FUENTE_TIMER)
fuente_pregunta = pygame.font.SysFont("timesnewroman", TAM_FUENTE_PREGUNTA)

# ICONOS
icono_sonido_on = pygame.transform.scale(pygame.image.load(RUTA_ICONO_SONIDO_ON), (40, 40))
icono_sonido_off = pygame.transform.scale(pygame.image.load(RUTA_ICONO_SONIDO_OFF), (40, 40))
icono_reset = pygame.transform.scale(pygame.image.load(RUTA_ICONO_RESET), (30, 30))
rect_icono_sonido = icono_sonido_on.get_rect(topright=(ANCHO_PANTALLA, 10))

# MÚSICA
pygame.mixer.music.load(RUTA_MUSICA_MENU)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# TIMER
evento_tick = pygame.USEREVENT + 3
pygame.time.set_timer(evento_tick, 1000)
segundos = 0

pantalla_actual = "MENU"
musica_activa = True

botones_menu = ["JUGAR", "PUNTAJES", "CONFIGURACIÓN", "SALIR"]
botones_configuracion = ["DIMENSIONES", "SONIDO", "VOLVER"]
desarrolladores = ["Martín Estevez", "Nicolas Rial Dell Anna", "Tomas Gil"]

# Juego
lista_preguntas = []
indices_preguntas = []
preguntas_respondidas = 0
pregunta_actual = None
respuestas_actuales = []
respuesta_correcta = ""
botones_respuesta = []
respuestas_correctas = 0

# Comodines
nombres_comodines = ["50/50", "CAMBIAR"]
botones_comodines = []
comodin_oculto = False

corriendo = True

while corriendo: # BUCLE PRINCIPAL

    for evento in pygame.event.get(): # EVENTO PARA CERRAR
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == evento_tick: # EVENTO PARA EL TIMER
            if pantalla_actual == "EN_JUEGO":
                segundos += 1

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # EVENTO PARA CLICK IZQUIERDO
            mouse_pos = pygame.mouse.get_pos() # Obtener la posición del mouse

            if rect_icono_sonido.collidepoint(mouse_pos): # Si se hace click en el icono de sonido
                if musica_activa == True:
                    musica_activa = False
                    pygame.mixer.music.set_volume(0.0) # Silenciar música
                else:
                    musica_activa = True
                    pygame.mixer.music.set_volume(0.5) # Reanudar música

            if pantalla_actual == "MENU": # Pantalla del menú

                x = (ANCHO_PANTALLA - ANCHO_BOTON) / 2

                for i in range(len(botones_menu)): # Iterar sobre los botones del menú

                    y = Y_BOTONES + i * (ALTO_BOTON + ESPACIO_ENTRE_BOTONES)

                    if pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON).collidepoint(mouse_pos):

                        if botones_menu[i] == "SALIR": # Salir del juego
                            corriendo = False

                        elif botones_menu[i] == "JUGAR": # Iniciar el juego
                            pantalla_actual = "EN_JUEGO"
                            segundos = 0 # Reiniciar el timer
                            respuestas_correctas = 0 # Reiniciar el contador de respuestas correctas
                            preguntas_respondidas = 0 # Reiniciar el contador de preguntas respondidas
                            lista_preguntas = leer_archivo_json("datos.json") # Cargar las preguntas del archivo JSON
                            indices_preguntas = crear_lista_indices_random(10, 0, len(lista_preguntas) - 1) # Crear una lista de índices aleatorios para las preguntas
                            pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]] # Obtener la primera pregunta
                            respuestas_actuales = obtener_respuestas(pregunta_actual) # Obtener las respuestas de la pregunta actual
                            respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta") # Obtener la respuesta correcta de la pregunta actual

                            
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

                for i in range(len(botones_respuesta)): # Iterar sobre los botones de respuesta
                    
                    if botones_respuesta[i].collidepoint(mouse_pos):
                        seleccion = respuestas_actuales[i] # Obtener la respuesta seleccionada

                        if seleccion == respuesta_correcta: # Si la respuesta es correcta
                            botones_respuesta[i] = dibujar_boton(pantalla, botones_respuesta[i], seleccion, fuente_boton, (0, 255, 0)) # Dibujar el botón de respuesta correcta en verde
                            respuestas_correctas += 1 # Incrementar el contador de respuestas correctas
                        preguntas_respondidas += 1 # Incrementar el contador de preguntas respondidas
                        
                        if preguntas_respondidas < 10: # Si aún hay preguntas por responder
                            pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]] # Obtener la siguiente pregunta
                            respuestas_actuales = obtener_respuestas(pregunta_actual) # Obtener las respuestas de la nueva pregunta
                            respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta") # Obtener la respuesta correcta de la nueva pregunta
                        else:
                            pantalla_actual = "JUEGO_TERMINADO" # Si se han respondido todas las preguntas, ir a la pantalla de juego terminado

            elif pantalla_actual == "JUEGO_TERMINADO":
                volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
                
                if volver_rect.collidepoint(mouse_pos):
                    pantalla_actual = "MENU"





    dibujar_fondo_por_pantalla(pantalla, pantalla_actual)

    #DIBUJAR CADA MENU

    if pantalla_actual == "MENU":
        
        dibujar_titulo(pantalla, "MENÚ PRINCIPAL", fuente_titulo, ANCHO_PANTALLA)

        dibujar_botones_menu(pantalla, botones_menu, fuente_boton, Y_BOTONES, ANCHO_BOTON, ALTO_BOTON, ESPACIO_ENTRE_BOTONES, ANCHO_PANTALLA)
        
        for i in range(len(desarrolladores)):
            texto = fuente_des.render(desarrolladores[i], True, COLOR_TEXTO)
            pantalla.blit(texto, (10, ALTO_PANTALLA - 120 + i * 30))


    elif pantalla_actual == "EN_JUEGO":
        
        dibujar_timer(pantalla, segundos, fuente_timer)
        
        dibujar_reset(pantalla, icono_reset)
        
        if pregunta_actual:
            
            dibujar_pregunta(pantalla, pregunta_actual["pregunta"], fuente_pregunta)
            
            botones_respuesta = dibujar_respuestas(pantalla, respuestas_actuales, fuente_boton)
        
        dibujar_boton(pantalla, pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40), "VOLVER", fuente_boton)

    elif pantalla_actual == "JUEGO_TERMINADO":
        
        dibujar_titulo(pantalla, "JUEGO TERMINADO", fuente_titulo, ANCHO_PANTALLA)

        mensaje = f"Respuestas correctas: {respuestas_correctas} de 10"
        texto = fuente_boton.render(mensaje, True, COLOR_TEXTO)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)))
        rect_volver = dibujar_boton_volver(pantalla, fuente_boton)

    pantalla.blit(icono_sonido_on if musica_activa else icono_sonido_off, rect_icono_sonido)

    pygame.display.update()

pygame.quit()
