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
fuente_marcadores = pygame.font.SysFont('timesnewroman', TAM_FUENTE_MARCADORES)
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
img_comodin_pausar_el_tiempo = pygame.image.load(RUTA_IMAGEN_COMODIN_PAUSAR_EL_TIEMPO)

img_comodin_5050 = pygame.transform.smoothscale(img_comodin_5050, (100, 140))
img_comodin_cambiar = pygame.transform.smoothscale(img_comodin_cambiar, (100, 140))
img_comodin_pausar_el_tiempo = pygame.transform.smoothscale(img_comodin_pausar_el_tiempo, (100, 140))

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
botones_configuracion = ["DIMENSIONES", "SONIDO"]
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

## Comodines
nombres_comodines = ["50/50", "CAMBIAR"]
botones_comodines = []
#bandera para activar los comodines
comodin_oculto = False
comodin_5050_usado = False
comodin_cambiar_usado = False
comodin_pausar_usado = False
comodin_usado = False

# Puntajes
puntaje_total = 0
puntaje_base = 100
tiempo_total = 0
datos_csv = leer_archivo("puntajes.csv")#cargar datos del archivo CSV
if datos_csv == None:#si no hay datos, inicializar lista vacía
    lista_jugadores  = []
else:
    lista_jugadores = cargar_datos(datos_csv)#cargar datos del archivo CSV

# NOMBRE
nombre_usuario = "" #declaración de variable para el nombre de usuario
input_activo = False #declaración de variable para controlar si el input está activo
pantalla_pide_nombre = False #pantalla que pide el nombre de usuario al finalizar el juego

corriendo = True

while corriendo:  # BUCLE PRINCIPAL

    for evento in pygame.event.get():  # EVENTO PARA CERRAR
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == evento_tick:  # EVENTO PARA EL TIMER
            if pantalla_actual == "EN_JUEGO" and not esperando_respuesta and not pausa:#se le agrego la condición de pausa
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
                            puntaje_total = 0           # <-- Reinicia el puntaje acumulado
                            tiempo_total = 0            # <-- Reinicia el tiempo total
                            nombre_usuario = ""         # <-- Reinicia el nombre de usuario si querés
                            pantalla_pide_nombre = False
                            input_activo = False
                            lista_preguntas = leer_archivo_json("datos.json")
                            indices_preguntas = crear_lista_indices_random(10, 0, len(lista_preguntas) - 1)
                            pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]]
                            respuestas_actuales = obtener_respuestas(pregunta_actual)
                            respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta")

                        elif botones_menu[i] == "PUNTAJES":
                            pantalla_actual = "PUNTAJES"
                            lista_puntajes = leer_puntajes_csv("puntajes.csv")


                        elif botones_menu[i] == "CONFIGURACIÓN":
                            pantalla_actual = "CONFIGURACIÓN"

            elif pantalla_actual == "PUNTAJES":
                volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
                if volver_rect.collidepoint(mouse_pos):
                    pantalla_actual = "MENU"

            elif pantalla_actual == "CONFIGURACIÓN":
                x = (ANCHO_PANTALLA - ANCHO_BOTON) / 2

                for i in range(len(botones_configuracion)):
                    y = Y_BOTONES + i * (ALTO_BOTON + ESPACIO_ENTRE_BOTONES)
                    if pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON).collidepoint(mouse_pos):
                        # Aquí podrías agregar lógica para otros botones de configuración si los agregas
                        pass

                # Detectar clic en el botón VOLVER (esquina inferior derecha)
                volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
                if volver_rect.collidepoint(mouse_pos):
                    pantalla_actual = "MENU"

            elif pantalla_actual == "EN_JUEGO":
                if not esperando_respuesta:
                    volver_rect = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
                    if volver_rect.collidepoint(mouse_pos):
                        pantalla_actual = "MENU"
                    if pygame.Rect(10, 10, 45, 45).collidepoint(mouse_pos):
                        segundos = 0
                    # --- Comodines ---
                    espacio = 40
                    ancho_comodin = img_comodin_5050.get_width()
                    alto_comodin = img_comodin_5050.get_height()
                    ancho_total = ancho_comodin * 3 + espacio * 2
                    x_inicial = (ANCHO_PANTALLA - ancho_total) // 2
                    y_comodin = ALTO_PANTALLA - alto_comodin - 20


                    # 50/50
                    x_5050 = x_inicial
                    rect_5050 = pygame.Rect(x_5050, y_comodin, ancho_comodin, alto_comodin)
                    if rect_5050 and rect_5050.collidepoint(mouse_pos) and not comodin_5050_usado and not comodin_usado:
                        # Lógica del comodín 50/50
                        respuestas_a_mostrar = [respuesta_correcta]
                        # Agrega una incorrecta aleatoria
                        incorrectas = [r for r in respuestas_actuales if r != respuesta_correcta]
                        if incorrectas:
                            import random
                            respuestas_a_mostrar.append(random.choice(incorrectas))
                        # Mezcla las dos respuestas a mostrar
                        random.shuffle(respuestas_a_mostrar)
                        respuestas_actuales = respuestas_a_mostrar
                        comodin_5050_usado = True
                        comodin_usado = True

                    # CAMBIAR
                    x_cambiar = x_inicial + ancho_comodin + espacio
                    rect_cambiar = pygame.Rect(x_cambiar, y_comodin, ancho_comodin, alto_comodin)
                    if rect_cambiar and rect_cambiar.collidepoint(mouse_pos) and not comodin_cambiar_usado and not comodin_usado:
                        # Cambiar la pregunta actual
                        preguntas_respondidas += 1
                        if preguntas_respondidas < 10:
                            pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]]
                            respuestas_actuales = obtener_respuestas(pregunta_actual)
                            respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta")
                            segundos = 0
                            comodin_cambiar_usado = True
                            comodin_usado = True
                        else:
                            pantalla_actual = "JUEGO_TERMINADO"
                            pantalla_pide_nombre = True

                    # PAUSAR TIEMPO
                    x_pausa = x_inicial + (ancho_comodin + espacio) * 2 
                    rect_pausa = pygame.Rect(x_pausa, y_comodin, ancho_comodin, alto_comodin)
                    if rect_pausa and rect_pausa.collidepoint(mouse_pos) and not comodin_pausar_usado and not comodin_usado:# se usa el comodín de pausar
                        # Pausar el tiempo
                        comodin_pausar_usado = True #activa el comodín de pausar el tiempo
                        comodin_usado = True #  bandera para controlar si se usó un comodín
                        pausa = True  # Pausa el timer

                    for i in range(len(botones_respuesta)):
                        if botones_respuesta[i].collidepoint(mouse_pos):
                            seleccion = respuestas_actuales[i] # Obtener la respuesta seleccionada
                            if seleccion == respuesta_correcta: # Si la respuesta es correcta
                                botones_respuesta[i] = dibujar_boton(pantalla, botones_respuesta[i], seleccion, fuente_boton, (0, 255, 0)) # verde
                                respuestas_correctas += 1
                                puntaje_total += calcular_puntaje(segundos, puntaje_base)
                            tiempo_total += segundos
                            esperando_respuesta = True 
                            tiempo_pausa = pygame.time.get_ticks()
                            preguntas_respondidas += 1
                            segundos = 0

            elif pantalla_actual == "JUEGO_TERMINADO":
                rect_volver = pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40)
                if rect_volver.collidepoint(mouse_pos):
                    pantalla_actual = "MENU"
                # Calcula igual que en el render
                y_inicio = 200
                marcador_1 = fuente_boton.render(f"Puntaje total: {puntaje_total}", True, COLOR_TEXTO)
                marcador_2 = fuente_boton.render(f"Tiempo: {tiempo_total} segundos", True, COLOR_TEXTO)
                marcador_3 = fuente_boton.render(f"Respuestas correctas: {respuestas_correctas}", True, COLOR_TEXTO)
                y_input = y_inicio + marcador_1.get_height() + marcador_2.get_height() + marcador_3.get_height() + 50
                input_rect = pygame.Rect((ANCHO_PANTALLA - 300) // 2, y_input, 300, 50)
                if input_rect.collidepoint(mouse_pos):
                    input_activo = True
                else:
                    input_activo = False

        if evento.type == pygame.KEYDOWN and input_activo and pantalla_pide_nombre:
            if evento.key == pygame.K_BACKSPACE:
                nombre_usuario = nombre_usuario[:-1]
            elif evento.key == pygame.K_RETURN:
                if nombre_usuario.strip() != "":
                    pantalla_pide_nombre = False
                    input_activo = False
                    # Guardar puntaje, tiempo y nombre al presionar Enter
                    actualizar_ranking(nombre_usuario, puntaje_total, tiempo_total, "puntajes.csv")
                    # REACTIVAR comodines al finalizar partida y guardar nombre
                    comodin_5050_usado = False#activa el comodín 50/50
                    comodin_cambiar_usado = False#activa el comodín de cambiar la pregunta
                    comodin_pausar_usado = False#activa el comodín de pausar el tiempo
                    comodin_usado = False#bandera para controlar si se usó un comodín
            elif len(nombre_usuario) < 20 and evento.unicode.isprintable():
                nombre_usuario += evento.unicode

    # LÓGICA DEL JUEGO
    if esperando_respuesta:
        if pygame.time.get_ticks() - tiempo_pausa >= 0000:  # 2000 ms = 2 segundos
            esperando_respuesta = False
            pausa = False  # <-- REANUDA el timer después de responder, incluso si venía de comodín
            if preguntas_respondidas < 10:
                pregunta_actual = lista_preguntas[indices_preguntas[preguntas_respondidas]]
                respuestas_actuales = obtener_respuestas(pregunta_actual)
                respuesta_correcta = (lambda d, c: d[c])(pregunta_actual, "correcta")
            else:
                pantalla_actual = "JUEGO_TERMINADO"
                pantalla_pide_nombre = True  # <-- Activa el input al terminar el juego
                input_activo = True
                #Guardar puntaje, tiempo y nombre si ya hay nombre
                if nombre_usuario.strip() != "":
                    actualizar_ranking(nombre_usuario, puntaje_total, tiempo_total, "puntajes.csv")

        else:
            dibujar_fondo_por_pantalla(pantalla, pantalla_actual)
            if pregunta_actual:
                dibujar_pregunta(pantalla, pregunta_actual["pregunta"], fuente_pregunta)
                botones_respuesta = []
                botones_temp = dibujar_respuestas(pantalla, respuestas_actuales, fuente_boton)
                for i in range(len(respuestas_actuales)):
                    respuesta = respuestas_actuales[i]
                    rect = botones_temp[i]
                    if respuesta == respuesta_correcta:
                        boton = dibujar_boton(pantalla, rect, respuesta, fuente_boton, (0, 255, 0), color_texto=(0,0,0))
                    else:
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
        # Botón VOLVER en la pantalla de configuración
        dibujar_boton(pantalla, pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40), "VOLVER", fuente_boton)
    
    elif pantalla_actual == "EN_JUEGO":
        dibujar_timer(pantalla, segundos, fuente_timer)
        dibujar_reset(pantalla, icono_reset)
        # Marcadores compactos en la esquina inferior izquierda
        marcador_puntaje = fuente_marcadores.render(f"PUNTAJE = {puntaje_total}", True, COLOR_TEXTO)
        if preguntas_respondidas > 0:
            porcentaje = int((respuestas_correctas / preguntas_respondidas) * 100)
        else:
            porcentaje = 0
        marcador_porcentaje = fuente_marcadores.render(f"% CORRECTAS = {porcentaje} %", True, COLOR_TEXTO)

        # Posiciones y tamaño compacto
        margen_x = 15
        margen_y = 15
        padding = 10
        espacio_textos = 5
        rect_ancho = max(marcador_puntaje.get_width(), marcador_porcentaje.get_width()) + 2 * padding
        rect_alto = marcador_puntaje.get_height() + marcador_porcentaje.get_height() + espacio_textos + 2 * padding

        rect = pygame.Rect(margen_x, ALTO_PANTALLA - rect_alto - margen_y, rect_ancho, rect_alto)
        pygame.draw.rect(pantalla, COLOR_FONDO_BOTON, rect)
        pygame.draw.rect(pantalla, (180, 180, 180), rect, 2)

        pantalla.blit(marcador_puntaje, (rect.x + padding, rect.y + padding))
        pantalla.blit(marcador_porcentaje, (rect.x + padding, rect.y + padding + marcador_puntaje.get_height() + espacio_textos))
        if pregunta_actual:
            dibujar_pregunta(pantalla, pregunta_actual["pregunta"], fuente_pregunta)
            botones_respuesta = dibujar_respuestas(pantalla, respuestas_actuales, fuente_boton)

            # DIBUJAR COMODINES: recorre la lista nombres_comodines
            espacio = 40
            ancho_comodin = img_comodin_5050.get_width()
            alto_comodin = img_comodin_5050.get_height()
            ancho_total = ancho_comodin * 3 + espacio * 2  # 3 imágenes + 2 espacios
            x_inicial = (ANCHO_PANTALLA - ancho_total) // 2
            y_comodin = ALTO_PANTALLA - alto_comodin - 20
            
            # 50/50
            x_5050 = x_inicial
            rect_5050 = pygame.Rect(x_5050, y_comodin, ancho_comodin, alto_comodin)
            pantalla.blit(img_comodin_5050, rect_5050)
            
            # CAMBIAR
            x_cambiar = x_inicial + ancho_comodin + espacio
            rect_cambiar = pygame.Rect(x_cambiar, y_comodin, ancho_comodin, alto_comodin)
            pantalla.blit(img_comodin_cambiar, rect_cambiar)

            # PAUSAR TIEMPO
            x_pausa = x_inicial + (ancho_comodin + espacio) * 2
            rect_pausa = pygame.Rect(x_pausa, y_comodin, ancho_comodin, alto_comodin)
            pantalla.blit(img_comodin_pausar_el_tiempo, rect_pausa)
            
        dibujar_boton(pantalla, pygame.Rect(ANCHO_PANTALLA - 170, ALTO_PANTALLA - 60, 150, 40), "VOLVER", fuente_boton)

    elif pantalla_actual == "JUEGO_TERMINADO":
        dibujar_titulo(pantalla, "JUEGO TERMINADO", fuente_titulo, ANCHO_PANTALLA)
        marcador_1 = fuente_boton.render(f"Puntaje total: {puntaje_total}", True, COLOR_TEXTO)
        marcador_2 = fuente_boton.render(f"Tiempo: {tiempo_total} segundos", True, COLOR_TEXTO)
        marcador_3 = fuente_boton.render(f"Respuestas correctas: {respuestas_correctas}", True, COLOR_TEXTO)

        # Ajusta este valor para dejar espacio debajo del título
        y_inicio = 200  # Por ejemplo, 120 píxeles desde arriba

        pantalla.blit(marcador_1, ((ANCHO_PANTALLA - marcador_1.get_width()) // 2, y_inicio))
        pantalla.blit(marcador_2, ((ANCHO_PANTALLA - marcador_2.get_width()) // 2, y_inicio + marcador_1.get_height() + 10))
        pantalla.blit(marcador_3, ((ANCHO_PANTALLA - marcador_3.get_width()) // 2, y_inicio + marcador_1.get_height() + marcador_2.get_height() + 20))
        rect_volver = dibujar_boton_volver(pantalla, fuente_boton)

        if pantalla_pide_nombre:
            y_input = y_inicio + marcador_1.get_height() + marcador_2.get_height() + marcador_3.get_height() + 50
            input_rect = pygame.Rect((ANCHO_PANTALLA - 300) // 2, y_input, 300, 50)
            color_input = (255, 255, 255) if input_activo else (200, 200, 200)
            pygame.draw.rect(pantalla, color_input, input_rect, border_radius=10)
            pygame.draw.rect(pantalla, (0, 0, 0), input_rect, 2, border_radius=10)
            texto_input = fuente_boton.render(nombre_usuario, True, (0, 0, 0))
            pantalla.blit(texto_input, (input_rect.x + 10, input_rect.y + 10))
            texto_label = fuente_des.render("Ingrese su nombre y presione Enter:", True, (255, 255, 255))
            label_rect = texto_label.get_rect(center=(input_rect.centerx, input_rect.y - 15))
            pantalla.blit(texto_label, label_rect)


    elif pantalla_actual == "PUNTAJES":
        ordenar_diccionarios(lista_puntajes, "puntaje", True)  # Ordena la lista de diccionarios por puntaje de manera descendente.
        dibujar_titulo(pantalla, "PUNTAJES", fuente_titulo, ANCHO_PANTALLA)
        dibujar_tabla_puntajes(pantalla, lista_puntajes, fuente_boton)
        dibujar_boton_volver(pantalla, fuente_boton)
    if musica_activa:
        pantalla.blit(icono_sonido_on, rect_icono_sonido)
    else:
        pantalla.blit(icono_sonido_off, rect_icono_sonido)

    pygame.display.update()

pygame.quit()