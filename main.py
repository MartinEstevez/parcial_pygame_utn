import pygame
from configuraciones import *
from funciones import *
from funciones_respuestas import *

pygame.init() # Inicializar Pygame
pygame.mixer.init() # Inicializar el mezclador de Pygame

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
img_comodin_5050 = pygame.image.load(RUTA_IMAGEN_COMODIN_50_50)
img_comodin_cambiar = pygame.image.load(RUTA_IMAGEN_COMODIN_CAMBIAR)

img_comodin_5050 = pygame.transform.smoothscale(img_comodin_5050, (100, 140))
img_comodin_cambiar = pygame.transform.smoothscale(img_comodin_cambiar, (100, 140))


# MÚSICA
pygame.mixer.music.load(RUTA_MUSICA_MENU)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# TIMER
evento_tick = pygame.USEREVENT + 3
pygame.time.set_timer(evento_tick, 1000)
segundos = 0
pausa = False #bandera para controlar la pausa del juego
esperando_respuesta = False #
tiempo_pausa = 0  #acumula en el que se pausa el juego


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

while corriendo:  # BUCLE PRINCIPAL

    for evento in pygame.event.get():  # EVENTO PARA CERRAR
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == evento_tick:  # EVENTO PARA EL TIMER
            if pantalla_actual == "EN_JUEGO" and not esperando_respuesta:#Cambiala condición del timer para que solo sume segundos si no está esperando respuesta:s
                segundos += 1 
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # CLICK IZQUIERDO
            mouse_pos = pygame.mouse.get_pos()

            if rect_icono_sonido.collidepoint(mouse_pos):
                if musica_activa:
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
                            segundos = 0
                            respuestas_correctas = 0
                            preguntas_respondidas = 0
                            lista_preguntas = leer_archivo_json("datos.json")
                            indices_preguntas = crear_lista_indices_random(10, 0, len(lista_preguntas) - 1)
                            pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]]
                            respuestas_actuales = obtener_respuestas(pregunta_actual)
                            respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta")

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
            #aca abajo esta la condicion que no permite hacer click en las respuestas cuando se esta esperando la respuesta
                if not esperando_respuesta:
                    volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
                    if volver_rect.collidepoint(mouse_pos):
                        pantalla_actual = "MENU"
                    if pygame.Rect(10, 10, 45, 45).collidepoint(mouse_pos):
                        segundos = 0
                    for i in range(len(botones_respuesta)): # Iterar sobre los botones de respuesta
                        
                        if botones_respuesta[i].collidepoint(mouse_pos):
                            seleccion = respuestas_actuales[i] # Obtener la respuesta seleccionada
                            #aca boton de colores cuando es correcto 
                            if seleccion == respuesta_correcta: # Si la respuesta es correcta
                                botones_respuesta[i] = dibujar_boton(pantalla, botones_respuesta[i], seleccion, fuente_boton, (0, 255, 0)) # Dibujar el botón de respuesta correcta en verde
                                respuestas_correctas += 1 # Incrementar el contador de respuestas correctas
                            #cuando se responde se activa la pausa y se guarda el tiempo de la pausa
                            esperando_respuesta = True 
                            tiempo_pausa = pygame.time.get_ticks()
                            preguntas_respondidas += 1 # Incrementar el contador de preguntas respondidas

            elif pantalla_actual == "JUEGO_TERMINADO":
                volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)

                if volver_rect.collidepoint(mouse_pos):
                    pantalla_actual = "MENU"

    # LÓGICA DEL JUEGO
    if esperando_respuesta:
        if pygame.time.get_ticks() - tiempo_pausa >= 3000:  # 3000 ms = 3 segundos #tiempo de espera para mostrar la respuesta correcta
            esperando_respuesta = False 
            if preguntas_respondidas < 10:
                pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]]
                respuestas_actuales = obtener_respuestas(pregunta_actual)
                respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta")
            else:
                pantalla_actual = "JUEGO_TERMINADO"
        else:
            # Mostrar mensaje de espera y resaltar respuestas en la misma posición
            dibujar_fondo_por_pantalla(pantalla, pantalla_actual)
            if pregunta_actual:
                dibujar_pregunta(pantalla, pregunta_actual["pregunta"], fuente_pregunta) 
                botones_respuesta = []
                botones_temp = dibujar_respuestas(pantalla, respuestas_actuales, fuente_boton)
                # Usar la misma lógica de posicionamiento que en dibujar_respuestas y preguntas de if para aca
                for i in range(len(respuestas_actuales)):
                    respuesta = respuestas_actuales[i]
                    rect = botones_temp[i]  # Usar el mismo rect que se usó para dibujar la pregunta
                    if respuesta == respuesta_correcta:#pinta en verde la respuesta correcta
                        boton = dibujar_boton(pantalla, rect, respuesta, fuente_boton, (0, 255, 0), color_texto=(0,0,0))
                    else:# pinta en rojo la respuesta incorrecta
                        boton = dibujar_boton(pantalla, rect, respuesta, fuente_boton, (200, 0, 0), color_texto=(255,255,255))
                    botones_respuesta.append(boton)
            dibujar_timer(pantalla, segundos, fuente_timer)
            dibujar_reset(pantalla, icono_reset)
            dibujar_boton(pantalla, pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40), "VOLVER", fuente_boton)
            pantalla.blit(icono_sonido_on if musica_activa else icono_sonido_off, rect_icono_sonido)
            pygame.display.update()
            continue  # Saltar el resto del bucle para evitar interacción 

    dibujar_fondo_por_pantalla(pantalla, pantalla_actual)

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

        if pregunta_actual:
            dibujar_pregunta(pantalla, pregunta_actual["pregunta"], fuente_pregunta)
            botones_respuesta = dibujar_respuestas(pantalla, respuestas_actuales, fuente_boton)

            # DIBUJAR COMODINES COMO IMÁGENES
            espacio = 40
            ancho_total = img_comodin_5050.get_width() + img_comodin_cambiar.get_width() + espacio
            x_inicial = (ANCHO_PANTALLA - ancho_total) // 2
            y_comodin = ALTO_PANTALLA - img_comodin_5050.get_height() - 20

            rect_5050 = pantalla.blit(img_comodin_5050, (x_inicial, y_comodin))
            rect_cambiar = pantalla.blit(img_comodin_cambiar, (x_inicial + img_comodin_5050.get_width() + espacio, y_comodin))

        dibujar_boton(pantalla, pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40), "VOLVER", fuente_boton)

    elif pantalla_actual == "JUEGO_TERMINADO":
        dibujar_titulo(pantalla, "JUEGO TERMINADO", fuente_titulo, ANCHO_PANTALLA)
        mensaje = f"Respuestas correctas: {respuestas_correctas} de 10"
        texto = fuente_boton.render(mensaje, True, COLOR_TEXTO)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)))
        rect_volver = dibujar_boton_volver(pantalla, fuente_boton)

    if musica_activa == True:
        pantalla.blit(icono_sonido_on, rect_icono_sonido)
    else:
        pantalla.blit(icono_sonido_off, rect_icono_sonido)

    pygame.display.update()


pygame.quit()
