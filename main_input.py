from funciones_respuestas import *

ruta = "clase_17/datos.json"
ruta_csv = "archivo.csv"

# VARIABLES
variable_respuesta = "correcta"
variable_pregunta = "pregunta"

# LISTAS
lista_diccionarios = leer_archivo_json(ruta)
datos_csv = leer_archivo(ruta_csv)
lista_jugadores = []

# MENSAJES
menu_comodines = """
[1] Llamar a un amigo
[2] Ocultar dos respuestas
[3] Cambiar pregunta

Ingrese el comodín que quiere utilizar: """

while True:
    lista_indices_random = crear_lista_indices_random(5, 0, len(lista_diccionarios) - 1)
    contador_correctas = 0
    acumuludador_puntos = 0
    comodines = True
    nombre_jugador = input("Ingrese nombre: ")
    
    for i in range(len(lista_indices_random)):
        mostrar_pregunta(lista_diccionarios[lista_indices_random[i]], variable_pregunta)
        mostrar_respuestas_aleatorias(lista_diccionarios[lista_indices_random[i]])

        if comodines == True:
            respuesta = input("Ingrese su respuesta ('0' para utilizar un comodín): ")

        else:
            respuesta = input("Ingrese su respuesta (no tienes comodines disponibles): ")

        if respuesta == "0" and comodines == True:
            while True:
                comodines = False
                opcion = input(menu_comodines)

                match opcion:
                    case "1":
                        print("Esta función no está disponible.")

                    case "2":
                        print("Comodín seleccionado: Ocultar dos respuestas\n")
                        mostrar_pregunta(lista_diccionarios[lista_indices_random[i]], variable_pregunta)
                        ocultar_respuestas(lista_diccionarios[lista_indices_random[i]], "correcta")
                        respuesta = input("Ingrese su respuesta: ")
                        if comprobar_respuesta(lista_diccionarios[lista_indices_random[i]], respuesta, variable_respuesta) == True:
                            print("Respuesta correcta.")
                            contador_correctas += 1
                            acumuludador_puntos += 10
                        else:
                            print("Respuesta incorrecta.")

                        break

                    case "3":
                        nueva_pregunta = cambiar_pregunta(lista_diccionarios, lista_indices_random, 0, len(lista_diccionarios) - 1)
                        mostrar_pregunta(nueva_pregunta, variable_pregunta)
                        mostrar_respuestas_aleatorias(nueva_pregunta)
                        respuesta = input("Ingrese su respuesta: ")

                        if comprobar_respuesta(nueva_pregunta, respuesta, variable_respuesta) == True:
                            print("Respuesta correcta.")
                            contador_correctas += 1
                            acumuludador_puntos += 10
                        else:
                            print("Respuesta incorrecta.")

                        break

                    case _:
                        print("Opción inválida.")

        else:
            if comprobar_respuesta(lista_diccionarios[lista_indices_random[i]], respuesta, variable_respuesta) == True:
                print("Respuesta correcta.")
                contador_correctas += 1
                acumuludador_puntos += 10


            else:
                print("Respuesta incorrecta.")

        print()
    
    contador_correctas = str(contador_correctas)
    acumuludador_puntos = str(acumuludador_puntos)
    lista_jugadores.append({"nombre":nombre_jugador,"correctas":contador_correctas,"puntaje":acumuludador_puntos})

    
    seguir_jugando = input("Quiere seguir jugando (si/no):  ") 
    while seguir_jugando != "no" and seguir_jugando != "si":
        print("Lo ingresado no es válido.")
        seguir_jugando = input("Quiere seguir jugando (si/no):  ") 

    if seguir_jugando == "no":
        print("Saliendo del programa..")
        break

print("Fin del juego.")
ordenar_diccionarios(lista_jugadores, "puntaje", descendente=True)
guardar_archivo (ruta_csv,"w",formatear_alumnos(lista_jugadores))
print("Puntajes guardados correctamente.")